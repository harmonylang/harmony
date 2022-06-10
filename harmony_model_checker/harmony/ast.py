import functools

from harmony_model_checker.harmony.code import Code
from harmony_model_checker.harmony.scope import Scope
from harmony_model_checker.harmony.state import State
from harmony_model_checker.harmony.ops import *
from harmony_model_checker.exception import *

labelcnt = 0
imported = {}           # imported modules
constants = {}          # constants modified with -c
used_constants = set()  # constants modified and used

class AST:
    def __init__(self, endtoken, token, atomically):
        # Check that token is of the form (lexeme, file, line, column)
        assert isinstance(token, tuple), token
        assert len(token) == 4, len(token)
        # No check b/c lexeme could be one of many types, e.g. int, str, bool, etc
        _, file, line, column = token
        assert isinstance(file, str), file
        assert isinstance(line, int), line
        assert isinstance(column, int), line
        self.endtoken = endtoken
        self.token = token
        self.atomically = atomically

    # a new local constant or tree of constants
    def define(self, scope, const):
        if isinstance(const, tuple):
            scope.checkUnused(const)
            (lexeme, file, line, column) = const
            scope.names[lexeme] = ("local-const", const)
        else:
            assert isinstance(const, list)
            for c in const:
                self.define(scope, c)

    # a new local variable or tree of variables
    def assign(self, scope, var):
        if isinstance(var, tuple):
            scope.checkUnused(var)
            (lexeme, file, line, column) = var
            scope.names[lexeme] = ("local-var", var)
        else:
            assert isinstance(var, list)
            for v in var:
                self.assign(scope, v)

    def delete(self, scope, code, var):
        assert False  # TODO: I think this is obsolete

    def isConstant(self, scope):
        return False

    def eval(self, scope, code):
        state = State(code, scope.labels)
        ctx = ContextValue(("__eval__", None, None, None), 0, emptytuple, emptydict)
        ctx.atomic = 1
        while ctx.pc != len(code.labeled_ops) and ctx.failure == None:
            code.labeled_ops[ctx.pc].op.eval(state, ctx)
        if ctx.failure != None:
            lexeme, file, line, column = self.token
            raise HarmonyCompilerError(
                message='constant evaluation failed: %s %s' % (self, ctx.failure),
                lexeme=lexeme,
                filename=file,
                line=line,
                column=column
            )
        return ctx.pop()

    def compile(self, scope, code):
        if self.isConstant(scope):
            code2 = Code()
            self.gencode(scope, code2)
            code2.append(ContinueOp(), self.token, self.endtoken)      # Hack: get endlabels evaluated
            code2.link()
            v = self.eval(scope, code2)
            code.append(PushOp((v, None, None, None)), self.token, self.endtoken)
        else:
            self.gencode(scope, code)

    # Return local var name if local access
    def localVar(self, scope):
        assert False, self

    # This is supposed to push the address of an lvalue
    def ph1(self, scope, code):
        lexeme, file, line, column = self.token
        raise HarmonyCompilerError(
            lexeme=lexeme,
            filename=file,
            line=line,
            column=column,
            message='Cannot use in left-hand side expression: %s' % str(self)
        )

    def gencode(self, scope: Scope, code: Code):
        assert False, self

    def doImport(self, scope, code, module):
        (lexeme, file, line, column) = module
        # assert lexeme not in scope.names        # TODO
        assert lexeme in imported, "Attempted to import " + str(lexeme) + ", but it is not found in imports: " + str(imported)

        scope.names[lexeme] = ("module", imported[lexeme])

    def getLabels(self):
        return set()

    def getImports(self):
        return []

    def accept_visitor(self, visitor, *args, **kwargs):
        assert False, self


class ComprehensionAST(AST):
    def __init__(self, endtoken, token, atomically, iter, value):
        super().__init__(endtoken, token, atomically)
        self.iter = iter
        self.value = value
    
    def rec_comprehension(self, scope, code, iter, pc, accu, ctype):
        if iter == []:
            if ctype in { "dict", "set", "list" }:
                code.append(LoadVarOp(accu), self.token, self.endtoken)
            (_, file, line, column) = self.token
            if ctype == "dict":
                self.key.compile(scope, code)
            self.value.compile(scope, code)
            if ctype == "set":
                code.append(NaryOp(("SetAdd", file, line, column), 2), self.token, self.endtoken)
                code.append(StoreVarOp(accu), self.token, self.endtoken)
            elif ctype == "dict":
                code.append(NaryOp(("DictAdd", file, line, column), 3), self.token, self.endtoken)
                code.append(StoreVarOp(accu), self.token, self.endtoken)
            elif ctype == "list":
                code.append(NaryOp(("ListAdd", file, line, column), 2), self.token, self.endtoken)
                code.append(StoreVarOp(accu), self.token, self.endtoken)
            return

        (type, rest) = iter[0]
        assert type == "for" or type == "where", type

        if type == "for":
            (var, var2, expr) = rest

            self.define(scope, var)
            if var2 != None:
                self.define(scope, var2)
            uid = len(code.labeled_ops)
            (lexeme, file, line, column) = self.token

            # Evaluate the collection over which to iterate
            expr.compile(scope, code)

            # Push the first index, which is 0
            code.append(PushOp((0, file, line, column)), self.token, self.endtoken)

            global labelcnt
            startlabel = LabelValue(None, "$%d_start" % labelcnt)
            endlabel = LabelValue(None, "$%d_end" % labelcnt)
            labelcnt += 1
            code.nextLabel(startlabel)
            code.append(CutOp(var, var2), self.token, self.endtoken)
            code.append(JumpCondOp(False, endlabel), self.token, self.endtoken)
            self.rec_comprehension(scope, code, iter[1:], startlabel, accu, ctype)
            code.append(JumpOp(startlabel), self.endtoken, self.endtoken)
            code.nextLabel(endlabel)

        else:
            assert type == "where"
            negate = isinstance(rest, NaryAST) and rest.op[0] == "not"
            cond = rest.args[0] if negate else rest
            cond.compile(scope, code)
            code.append(JumpCondOp(negate, pc), self.token, self.endtoken)
            self.rec_comprehension(scope, code, iter[1:], pc, accu, ctype)

    def comprehension(self, scope, code, ctype):
        ns = Scope(scope)
        # Keep track of the size
        uid = len(code.labeled_ops)
        (lexeme, file, line, column) = self.token
        accu = ("$accu%d"%len(code.labeled_ops), file, line, column)
        if ctype == "set":
            code.append(PushOp((SetValue(set()), file, line, column)), self.token, self.endtoken)
            code.append(StoreVarOp(accu), self.token, self.endtoken)
        elif ctype == "dict":
            code.append(PushOp((emptydict, file, line, column)), self.token, self.endtoken)  # LIST TOD
            code.append(StoreVarOp(accu), self.token, self.endtoken)
        elif ctype == "list":
            code.append(PushOp((emptytuple, file, line, column)), self.token, self.endtoken)
            code.append(StoreVarOp(accu), self.token, self.endtoken)
        self.rec_comprehension(ns, code, self.iter, None, accu, ctype)
        if ctype in { "set", "dict", "list" }:
            code.append(LoadVarOp(accu), self.token, self.endtoken)

class ConstantAST(AST):
    def __init__(self, endtoken, const):
        AST.__init__(self, endtoken, const, False)
        self.const = const

    def __repr__(self):
        return "ConstantAST" + str(self.const)

    def compile(self, scope, code):
        code.append(PushOp(self.const), self.token, self.endtoken)

    def isConstant(self, scope):
        return True

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_constant(self, *args, **kwargs)


class NameAST(AST):
    def __init__(self, endtoken, name):
        AST.__init__(self, endtoken, name, False)
        self.name = name

    def __repr__(self):
        return "NameAST" + str(self.name)

    def compile(self, scope, code):
        (t, v) = scope.lookup(self.name)
        if t in {"local-var", "local-const"}:
            code.append(LoadVarOp(self.name), self.token, self.endtoken)
        elif t == "constant":
            (lexeme, file, line, column) = self.name
            code.append(PushOp(v), self.token, self.endtoken)
        else:
            # TODO: should module lead to an error here?
            assert t in {"global", "module"}
            code.append(LoadOp(self.name, self.name, scope.prefix), self.token, self.endtoken)

    # TODO.  How about local-const?
    def localVar(self, scope):
        (t, v) = scope.lookup(self.name)
        assert t in {"constant", "local-var", "local-const", "global", "module"}
        return self.name[0] if t == "local-var" else None

    def ph1(self, scope, code):
        (t, v) = scope.lookup(self.name)
        if t in {"constant", "local-const"}:
            (lexeme, file, line, column) = v
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="constant cannot be an lvalue: %s" % str(self.name),
            )
        elif t == "local-var":
            (lexeme, file, line, column) = v
            if lexeme != "_":
                code.append(PushOp((AddressValue([lexeme]), file, line, column)), self.token, self.endtoken)
        else:
            (lexeme, file, line, column) = self.name
            if scope.prefix == None:
                code.append(PushOp((AddressValue([lexeme]), file, line, column)), self.token, self.endtoken)
            else:
                code.append(PushOp((AddressValue([scope.prefix + '$' + lexeme]), file, line, column)), self.token, self.endtoken)

    def ph2(self, scope, code, skip):
        if skip > 0:
            code.append(MoveOp(skip + 2), self.token, self.endtoken)
            code.append(MoveOp(2), self.token, self.endtoken)
        (t, v) = scope.lookup(self.name)
        if t == "local-var":
            if self.name[0] == "_":
                code.append(PopOp(), self.token, self.endtoken)
            else:
                code.append(StoreVarOp(None, self.name[0]), self.token, self.endtoken)
        else:
            assert t == "global", (t, v)
            code.append(StoreOp(None, self.name, None), self.token, self.endtoken)

    def isConstant(self, scope):
        (lexeme, file, line, column) = self.name
        (t, v) = scope.lookup(self.name)
        if t in {"local-var", "local-const", "global", "module"}:
            return False
        elif t == "constant":
            return not isinstance(v[0], LabelValue)
        else:
            assert False, (t, v, self.name)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_name(self, *args, **kwargs)


class SetAST(AST):
    def __init__(self, endtoken, token, collection):
        AST.__init__(self, endtoken, token, False)
        self.collection = collection

    def __repr__(self):
        return str(self.collection)

    def isConstant(self, scope):
        return all(x.isConstant(scope) for x in self.collection)

    def gencode(self, scope, code):
        code.append(PushOp((SetValue(set()), None, None, None)), self.token, self.endtoken)
        for e in self.collection:
            e.compile(scope, code)
            code.append(NaryOp(("SetAdd", None, None, None), 2), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_set(self, *args, **kwargs)


class RangeAST(AST):
    def __init__(self, endtoken, lhs, rhs, token):
        AST.__init__(self, endtoken, token, False)
        self.lhs = lhs
        self.rhs = rhs

    def __repr__(self):
        return "Range(%s,%s)" % (self.lhs, self.rhs)

    def isConstant(self, scope):
        return self.lhs.isConstant(scope) and self.rhs.isConstant(scope)

    def gencode(self, scope, code):
        self.lhs.compile(scope, code)
        self.rhs.compile(scope, code)
        (lexeme, file, line, column) = self.token
        code.append(NaryOp(("..", file, line, column), 2), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_range(self, *args, **kwargs)


class TupleAST(AST):
    def __init__(self, endtoken, list, token):
        AST.__init__(self, endtoken, token, False)
        self.list = list

    def __repr__(self):
        return "TupleAST" + str(self.list)

    def isConstant(self, scope):
        return all(v.isConstant(scope) for v in self.list)

    def gencode(self, scope, code):
        (lexeme, file, line, column) = self.token
        code.append(PushOp((emptytuple, file, line, column)), self.token, self.endtoken)
        for v in self.list:
            v.compile(scope, code)
            code.append(NaryOp(("ListAdd", file, line, column), 2), self.token, self.endtoken)

    def localVar(self, scope):
        lexeme, file, line, column = self.token
        raise HarmonyCompilerError(
            message="Cannot index into tuple in assignment",
            lexeme=lexeme,
            filename=file,
            line=line,
            column=column
        )

    def ph1(self, scope, code):
        for lv in self.list:
            lv.ph1(scope, code)

    def ph2(self, scope, code, skip):
        n = len(self.list)
        code.append(SplitOp(n), self.token, self.endtoken)
        for lv in reversed(self.list):
            n -= 1
            lv.ph2(scope, code, skip + n)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_tuple(self, *args, **kwargs)


class DictAST(AST):
    def __init__(self, endtoken, token, record):
        AST.__init__(self, endtoken, token, False)
        self.record = record

    def __repr__(self):
        return "DictAST" + str(self.record)

    def isConstant(self, scope):
        return all(k.isConstant(scope) and v.isConstant(scope)
                   for (k, v) in self.record)

    def gencode(self, scope, code):
        code.append(PushOp((emptydict, None, None, None)), self.token, self.endtoken)
        for (k, v) in self.record:
            k.compile(scope, code)
            v.compile(scope, code)
            code.append(NaryOp(("DictAdd", None, None, None), 3), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_dict(self, *args, **kwargs)


class SetComprehensionAST(ComprehensionAST):
    def __init__(self, endtoken, value, iter, token):
        super().__init__(endtoken, token, False, iter, value)

    def __repr__(self):
        return "SetComprehension(" + str(self.iter) + "," + str(self.value) + ")"

    def compile(self, scope, code):
        self.comprehension(scope, code, "set")

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_set_comprehension(self, *args, **kwargs)


class DictComprehensionAST(ComprehensionAST):
    def __init__(self, endtoken, key, value, iter, token):
        super().__init__(endtoken, token, False, iter, value)
        self.key = key

    def __repr__(self):
        return "DictComprehension(" + str(self.key) + ")"

    def compile(self, scope, code):
        self.comprehension(scope, code, "dict")

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_dict_comprehension(self, *args, **kwargs)


class ListComprehensionAST(ComprehensionAST):
    def __init__(self, endtoken, value, iter, token):
        super().__init__(endtoken, token, False, iter, value)

    def __repr__(self):
        return "ListComprehension(" + str(self.value) + ")"

    def compile(self, scope, code):
        self.comprehension(scope, code, "list")

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_list_comprehension(self, *args, **kwargs)


# N-ary operator
class NaryAST(AST):
    def __init__(self, endtoken, token, op, args):
        AST.__init__(self, endtoken, token, False)
        self.op = op
        self.args = args
        assert all(isinstance(x, AST) for x in args), args

    def __repr__(self):
        return "NaryOp(" + str(self.op) + ", " + str(self.args) + ")"

    def isConstant(self, scope):
        (op, file, line, column) = self.op
        if op in {"atLabel", "choose", "contexts", "countLabel", "get_context"}:
            return False
        return all(x.isConstant(scope) for x in self.args)

    def gencode(self, scope, code):
        global labelcnt
        (op, file, line, column) = self.op
        n = len(self.args)
        if op == "and" or op == "or":
            self.args[0].compile(scope, code)
            lastlabel = LabelValue(None, "$%d_last" % labelcnt)
            endlabel = LabelValue(None, "$%d_end" % labelcnt)
            labelcnt += 1
            for i in range(1, n):
                code.append(JumpCondOp(op == "or", lastlabel), self.token, self.endtoken)
                self.args[i].compile(scope, code)
            code.append(JumpOp(endlabel), self.op, self.op)
            code.nextLabel(lastlabel)
            code.append(PushOp((op == "or", file, line, column)), self.token, self.endtoken)
            code.nextLabel(endlabel)
        elif op == "=>":
            assert n == 2, n
            self.args[0].compile(scope, code)
            truelabel = LabelValue(None, "$%d_true" % labelcnt)
            endlabel = LabelValue(None, "$%d_end" % labelcnt)
            labelcnt += 1
            code.append(JumpCondOp(False, truelabel), self.token, self.endtoken)
            self.args[1].compile(scope, code)
            code.append(JumpOp(endlabel), self.op, self.op)
            code.nextLabel(truelabel)
            code.append(PushOp((True, file, line, column)), self.token, self.endtoken)
            code.nextLabel(endlabel)
        elif op == "if":
            assert n == 3, n
            negate = isinstance(self.args[1], NaryAST) and self.args[1].op[0] == "not"
            cond = self.args[1].args[0] if negate else self.args[1]
            cond.compile(scope, code)
            elselabel = LabelValue(None, "$%d_else" % labelcnt)
            endlabel = LabelValue(None, "$%d_end" % labelcnt)
            labelcnt += 1
            code.append(JumpCondOp(negate, elselabel), self.token, self.endtoken)
            self.args[0].compile(scope, code)  # "if" expr
            code.append(JumpOp(endlabel), self.op, self.op)
            code.nextLabel(elselabel)
            self.args[2].compile(scope, code)  # "else" expr
            code.nextLabel(endlabel)
        elif op == "choose":
            assert n == 1
            self.args[0].compile(scope, code)
            code.append(ChooseOp(), self.token, self.endtoken)
        else:
            for i in range(n):
                self.args[i].compile(scope, code)
            code.append(NaryOp(self.op, n), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_nary(self, *args, **kwargs)


class CmpAST(AST):
    def __init__(self, endtoken, token, ops, args):
        AST.__init__(self, endtoken, token, False)
        self.ops = ops
        self.args = args
        assert len(ops) == len(args) - 1
        assert all(isinstance(x, AST) for x in args), args

    def __repr__(self):
        return "CmpOp(" + str(self.ops) + ", " + str(self.args) + ")"

    def isConstant(self, scope):
        return all(x.isConstant(scope) for x in self.args)

    def gencode(self, scope, code):
        n = len(self.args)
        self.args[0].compile(scope, code)
        (lexeme, file, line, column) = self.ops[0]
        T = ("__cmp__" + str(len(code.labeled_ops)), file, line, column)
        endlabel = LabelValue(None, "cmp$%d"%len(code.labeled_ops))
        for i in range(1, n - 1):
            self.args[i].compile(scope, code)
            code.append(DupOp(), self.token, self.endtoken)
            code.append(StoreVarOp(T), self.token, self.endtoken)
            code.append(NaryOp(self.ops[i - 1], 2), self.token, self.endtoken)
            code.append(DupOp(), self.token, self.endtoken)
            code.append(JumpCondOp(False, endlabel), self.token, self.endtoken)
            code.append(PopOp(), self.token, self.endtoken)
            code.append(LoadVarOp(T), self.token, self.endtoken)
        self.args[n - 1].compile(scope, code)
        code.append(NaryOp(self.ops[n - 2], 2), self.token, self.endtoken)
        code.nextLabel(endlabel)
        if n > 2:
            code.append(DelVarOp(T), self.token, self.endtoken)     # TODO: is this necessary???

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_cmp(self, *args, **kwargs)


class ApplyAST(AST):
    def __init__(self, endtoken, method, arg, token):
        AST.__init__(self, endtoken, token, False)
        self.method = method
        self.arg = arg

    def __repr__(self):
        return "ApplyAST(" + str(self.method) + ", " + str(self.arg) + ")"

    def varCompile(self, scope, code):
        if isinstance(self.method, NameAST):
            (t, v) = scope.lookup(self.method.name)
            if t == "global":
                self.method.ph1(scope, code)
                self.arg.compile(scope, code)
                code.append(AddressOp(), self.token, self.endtoken)
                return True
            else:
                return False

        if isinstance(self.method, PointerAST):
            self.method.expr.compile(scope, code)
            self.arg.compile(scope, code)
            code.append(AddressOp(), self.token, self.endtoken)
            return True

        if isinstance(self.method, ApplyAST):
            if self.method.varCompile(scope, code):
                self.arg.compile(scope, code)
                code.append(AddressOp(), self.token, self.endtoken)
                return True
            else:
                return False

        return False

    def compile(self, scope, code):
        if isinstance(self.method, NameAST):
            (t, v) = scope.lookup(self.method.name)
            # See if it's of the form "module.constant":
            if t == "module" and isinstance(self.arg, ConstantAST) and isinstance(self.arg.const[0], str):
                (t2, v2) = v.lookup(self.arg.const)
                if t2 == "constant":
                    code.append(PushOp(v2), self.token, self.endtoken)
                    return
            # Decrease chances of data race
            if t == "global":
                self.method.ph1(scope, code)
                self.arg.compile(scope, code)
                code.append(AddressOp(), self.token, self.endtoken)
                code.append(LoadOp(None, self.token, None), self.token, self.endtoken)
                return

        # Decrease chances of data race
        if self.varCompile(scope, code):
            code.append(LoadOp(None, self.token, None), self.token, self.endtoken)
            return

        self.method.compile(scope, code)
        self.arg.compile(scope, code)
        code.append(ApplyOp(self.token), self.token, self.endtoken)

    def localVar(self, scope):
        return self.method.localVar(scope)

    def ph1(self, scope, code):
        # See if it's of the form "module.constant":
        if isinstance(self.method, NameAST):
            (t, v) = scope.lookup(self.method.name)
            if t == "module" and isinstance(self.arg, ConstantAST) and isinstance(self.arg.const[0], str):
                (t2, v2) = v.lookup(self.arg.const)
                if t2 == "constant":
                    lexeme, file, line, column = self.token
                    raise HarmonyCompilerError(
                        message="Cannot assign to constant %s %s" % (self.method.name, self.arg.const),
                        lexeme=lexeme,
                        filename=file,
                        line=line,
                        column=column
                    )
        self.method.ph1(scope, code)
        self.arg.compile(scope, code)
        code.append(AddressOp(), self.token, self.endtoken)

    def ph2(self, scope, code, skip):
        if skip > 0:
            code.append(MoveOp(skip + 2), self.token, self.endtoken)
            code.append(MoveOp(2), self.token, self.endtoken)
        lvar = self.method.localVar(scope)
        st = StoreOp(None, self.token, None) if lvar == None else StoreVarOp(None, lvar)
        code.append(st, self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_apply(self, *args, **kwargs)


class PointerAST(AST):
    def __init__(self, endtoken, expr, token):
        AST.__init__(self, endtoken, token, False)
        self.expr = expr

    def __repr__(self):
        return "PointerAST(" + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(LoadOp(None, self.token, None), self.token, self.endtoken)

    def localVar(self, scope):
        return None

    def ph1(self, scope, code):
        self.expr.compile(scope, code)

    def ph2(self, scope, code, skip):
        if skip > 0:
            code.append(MoveOp(skip + 2), self.token, self.endtoken)
            code.append(MoveOp(2), self.token, self.endtoken)
        code.append(StoreOp(None, self.token, None), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_pointer(self, *args, **kwargs)


class AssignmentAST(AST):
    def __init__(self, endtoken, token, lhslist, rv, op, atomically):
        AST.__init__(self, endtoken, token, atomically)
        self.lhslist = lhslist  # a, b = c, d = e = ...
        self.rv = rv  # rhs expression
        self.op = op  # ... op= ...

    def __repr__(self):
        return "Assignment(" + str(self.lhslist) + ", " + str(self.rv) + \
               ", " + str(self.op) + ")"

    # handle an "x op= y" assignment
    def opassign(self, lv, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        lvar = lv.localVar(scope)
        if isinstance(lv, NameAST):
            # handled separately for assembly code readability
            (t, v) = scope.lookup(lv.name)
            lexeme, file, line, column = self.token
            if t == "module":
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message='Cannot operate on module %s' % str(lv.name),
                )
            if t in {"constant", "local-const"}:
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message='Cannot operate on constant %s' % str(lv.name),
                )
            assert t in {"local-var", "global"}
            ld = LoadOp(lv.name, lv.name, scope.prefix) if t == "global" else LoadVarOp(lv.name)
        else:
            lv.ph1(scope, code)
            code.append(DupOp(), self.token, self.endtoken)  # duplicate the addres
            ld = LoadOp(None, self.op, None) if lvar == None else LoadVarOp(None, lvar)
        code.append(ld, self.token, self.endtoken)  # load the valu
        self.rv.compile(scope, code)  # compile the rhs
        (lexeme, file, line, column) = self.op
        code.append(NaryOp((lexeme[:-1], file, line, column), 2), self.token, self.endtoken)
        if isinstance(lv, NameAST):
            st = StoreOp(lv.name, lv.name, scope.prefix) if lvar == None else StoreVarOp(lv.name, lvar)
        else:
            st = StoreOp(None, self.op, None) if lvar == None else StoreVarOp(None, lvar)
        code.append(st, self.token, self.op)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def compile(self, scope, code):
        (lexeme, file, line, column) = self.op
        if lexeme != '=':
            assert len(self.lhslist) == 1, self.lhslist
            lv = self.lhslist[0]
            self.opassign(lv, scope, code)
            return

        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)

        # Compute the addresses of lhs expressions
        for lvs in self.lhslist:
            # handled separately for better assembly code readability
            if not isinstance(lvs, NameAST):
                lvs.ph1(scope, code)

        # Compute the right-hand side
        self.rv.compile(scope, code)

        # Make enough copies for each left-hand side
        for i in range(len(self.lhslist) - 1):
            code.append(DupOp(), self.token, self.endtoken)

        # Now assign to the left-hand side in reverse order
        skip = len(self.lhslist)
        for lvs in reversed(self.lhslist):
            skip -= 1
            if isinstance(lvs, NameAST):
                (t, v) = scope.lookup(lvs.name)
                if t == "module":
                    raise HarmonyCompilerError(
                        lexeme=lexeme,
                        filename=file,
                        line=line,
                        column=column,
                        message='Cannot assign to module %s' % str(lvs.name),
                    )
                if t in {"constant", "local-const"}:
                    raise HarmonyCompilerError(
                        lexeme=lexeme,
                        filename=file,
                        line=line,
                        column=column,
                        message='Cannot assign to constant %s' % str(lvs.name),
                    )
                assert t in {"local-var", "global"}, (t, lvs.name)
                if v[0] == "_":
                    code.append(PopOp(), self.token, self.endtoken)
                else:
                    st = StoreOp(lvs.name, lvs.name, scope.prefix) if t == "global" else StoreVarOp(lvs.name)
                    code.append(st, self.token, self.endtoken)
            else:
                lvs.ph2(scope, code, skip)

        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_assignment(self, *args, **kwargs)


class DelAST(AST):
    def __init__(self, endtoken, token, atomically, lv):
        AST.__init__(self, endtoken, token, atomically)
        self.lv = lv

    def __repr__(self):
        return "Del(" + str(self.lv) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        lvar = self.lv.localVar(scope)
        if isinstance(self.lv, NameAST):
            op = DelOp(self.lv.name, scope.prefix) if lvar == None else DelVarOp(self.lv.name)
        else:
            self.lv.ph1(scope, code)
            op = DelOp(None, None) if lvar == None else DelVarOp(None, lvar)
        code.append(op, self.token, self.endtoken)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_del(self, *args, **kwargs)


class SetIntLevelAST(AST):
    def __init__(self, endtoken, token, arg):
        AST.__init__(self, endtoken, token, False)
        self.arg = arg

    def __repr__(self):
        return "SetIntLevel " + str(self.arg)

    def compile(self, scope, code):
        self.arg.compile(scope, code)
        code.append(SetIntLevelOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_set_int_level(self, *args, **kwargs)


class SaveAST(AST):
    def __init__(self, endtoken, token, expr):
        AST.__init__(self, endtoken, token, False)
        self.expr = expr

    def __repr__(self):
        return "Save " + str(self.expr)

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(SaveOp(), self.token, self.endtoken)
        code.append(ContinueOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_save(self, *args, **kwargs)


class StopAST(AST):
    def __init__(self, endtoken, token, expr):
        AST.__init__(self, endtoken, token, False)
        self.expr = expr

    def __repr__(self):
        return "Stop " + str(self.expr)

    def compile(self, scope, code):
        # self.expr.ph1(scope, code)
        self.expr.compile(scope, code)
        code.append(StopOp(None), self.token, self.endtoken)
        code.append(ContinueOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_stop(self, *args, **kwargs)


class AddressAST(AST):
    def __init__(self, endtoken, token, lv):
        AST.__init__(self, endtoken, token, False)
        self.lv = lv

    def __repr__(self):
        return "Address(" + str(self.lv) + ")"

    def isConstant(self, scope):
        return self.lv.isConstant(scope)

    def check(self, lv, scope):
        if isinstance(lv, NameAST):
            (t, v) = scope.lookup(lv.name)
            lexeme, file, line, column = lv.name
            if t in {"local-var", "local-const"}:
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Can't take address of local variable %s" % str(lv),
                )
            if t == "constant":
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Can't take address of constant %s" % str(lv),
                )
            if t == "module":
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="Can't take address of imported %s" % str(lv),
                )
        elif isinstance(lv, ApplyAST):
            self.check(lv.method, scope)
        elif isinstance(lv, PointerAST):
            pass
        else:
            lexeme, file, line, column = lv.token if isinstance(lv, AST) else (None, None, None, None)
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="Can't take address of %s" % str(lv),
            )

    def gencode(self, scope, code):
        self.check(self.lv, scope)
        self.lv.ph1(scope, code)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_address(self, *args, **kwargs)


class PassAST(AST):
    def __init__(self, endtoken, token, atomically):
        AST.__init__(self, endtoken, token, atomically)

    def __repr__(self):
        return "Pass"

    def compile(self, scope, code):
        pass

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_pass(self, *args, **kwargs)


class BlockAST(AST):
    def __init__(self, endtoken, token, atomically, b):
        AST.__init__(self, endtoken, token, atomically)
        assert len(b) > 0
        self.b = b

    def __repr__(self):
        return "Block(" + str(self.b) + ")"

    def compile(self, scope, code):
        ns = Scope(scope)
        for s in self.b:
            for ((lexeme, file, line, column), lb) in s.getLabels():
                ns.names[lexeme] = ("constant", (lb, file, line, column))
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        for s in self.b:
            s.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)
        if scope.inherit:
            for name, x in ns.names.items():
                scope.names[name] = x

    def getLabels(self):
        labels = [x.getLabels() for x in self.b]
        return functools.reduce(lambda x, y: x | y, labels)

    def getImports(self):
        imports = [x.getImports() for x in self.b]
        return functools.reduce(lambda x, y: x + y, imports)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_block(self, *args, **kwargs)


class IfAST(AST):
    def __init__(self, endtoken, token, atomically, alts, stat):
        AST.__init__(self, endtoken, token, atomically)
        self.alts = alts  # alternatives
        self.stat = stat  # else statement

    def __repr__(self):
        return "If(" + str(self.alts) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        global labelcnt
        label = labelcnt
        labelcnt += 1
        sublabel = 0
        endlabel = LabelValue(None, "$%d_end" % label)
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        last = len(self.alts) - 1
        for i, alt in enumerate(self.alts):
            (rest, stat, starttoken, endtoken) = alt
            code.location(starttoken[1], starttoken[2])
            negate = isinstance(rest, NaryAST) and rest.op[0] == "not"
            cond = rest.args[0] if negate else rest
            cond.compile(scope, code)
            iflabel = LabelValue(None, "$%d_%d" % (label, sublabel))
            code.append(JumpCondOp(negate, iflabel), starttoken, starttoken)
            sublabel += 1
            stat.compile(scope, code)
            if self.stat != None or i != last:
                code.append(JumpOp(endlabel), endtoken, endtoken)
            code.nextLabel(iflabel)
        if self.stat != None:
            self.stat.compile(scope, code)
        code.nextLabel(endlabel)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def getLabels(self):
        labels = [x.getLabels() for (c, x, _, _) in self.alts]
        if self.stat != None:
            labels += [self.stat.getLabels()]
        return functools.reduce(lambda x, y: x | y, labels)

    def getImports(self):
        imports = [x.getImports() for (c, x, _, _) in self.alts]
        if self.stat != None:
            imports += [self.stat.getImports()]
        return functools.reduce(lambda x, y: x + y, imports)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_if(self, *args, **kwargs)


class WhileAST(AST):
    def __init__(self, endtoken, token, atomically, cond, stat):
        AST.__init__(self, endtoken, token, atomically)
        self.cond = cond
        self.stat = stat

    def __repr__(self):
        return "While(" + str(self.cond) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        negate = isinstance(self.cond, NaryAST) and self.cond.op[0] == "not"
        cond = self.cond.args[0] if negate else self.cond
        global labelcnt
        startlabel = LabelValue(None, "$%d_start" % labelcnt)
        endlabel = LabelValue(None, "$%d_end" % labelcnt)
        labelcnt += 1
        code.nextLabel(startlabel)
        cond.compile(scope, code)
        code.append(JumpCondOp(negate, endlabel), self.token, self.endtoken)
        self.stat.compile(scope, code)
        code.append(JumpOp(startlabel), self.endtoken, self.endtoken)
        code.nextLabel(endlabel)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def getLabels(self):
        return self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_while(self, *args, **kwargs)


class InvariantAST(AST):
    def __init__(self, endtoken, cond, token, atomically):
        AST.__init__(self, endtoken, token, atomically)
        self.cond = cond

    def __repr__(self):
        return "Invariant(" + str(self.cond) + ")"

    def compile(self, scope, code):
        global labelcnt
        label = LabelValue(None, "$%d" % labelcnt)
        labelcnt += 1
        code.append(InvariantOp(label, self.token), self.token, self.endtoken)
        self.cond.compile(scope, code)

        # TODO. The following is a workaround for a bug.
        # When you do "invariant 0 <= count <= 1", it inserts
        # DelVar operations before the ReturnOp, and the InvariantOp
        # operation then jumps to the wrong instruction
        code.append(ContinueOp(), self.token, self.endtoken)

        code.nextLabel(label)
        code.append(ReturnOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_invariant(self, *args, **kwargs)


class LetAST(AST):
    def __init__(self, endtoken, token, atomically, vars, stat):
        AST.__init__(self, endtoken, token, atomically)
        self.vars = vars
        self.stat = stat

    def __repr__(self):
        return "Let(" + str(self.vars) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        ns = Scope(scope)
        for (var, expr) in self.vars:
            expr.compile(ns, code)
            code.append(StoreVarOp(var), self.token, self.endtoken)
            self.define(ns, var)

        # Run the body
        self.stat.compile(ns, code)

        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_let(self, *args, **kwargs)


class VarAST(AST):
    def __init__(self, endtoken, token, atomically, vars):
        AST.__init__(self, endtoken, token, atomically)
        self.vars = vars

    def __repr__(self):
        return "Var(" + str(self.vars) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        for (var, expr) in self.vars:
            expr.compile(scope, code)
            code.append(StoreVarOp(var), self.token, self.endtoken)
            self.assign(scope, var)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_var(self, *args, **kwargs)


class ForAST(ComprehensionAST):
    def __init__(self, endtoken, iter, stat, token, atomically):
        super().__init__(endtoken, token, atomically, iter, stat)

    def __repr__(self):
        return "For(" + str(self.iter) + ", " + str(self.value) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        ns = Scope(scope)
        self.comprehension(ns, code, "for")
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def getLabels(self):
        return self.value.getLabels()

    def getImports(self):
        return self.value.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_for(self, *args, **kwargs)


class LetWhenAST(AST):
    # vars_and_conds, a list of one of
    #   - ('var', bv, ast)              // let bv = ast
    #   - ('cond', cond)                // when cond:
    #   - ('exists', bv, expr)    // when exists bv in expr
    def __init__(self, endtoken, token, atomically, vars_and_conds, stat):
        AST.__init__(self, endtoken, token, atomically)
        self.vars_and_conds = vars_and_conds
        self.stat = stat

    def __repr__(self):
        return "LetWhen(" + str(self.vars_and_conds) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        """
        start:
            atomic inc
            [[let1]]
            [[cond1]]
            jump condfailed if false
            ...
            [[letn]]
            [[condn]]
            jump condfailed if false
            jump body
        condfailed:
            atomic dec
            jump start
        select:
            choose
            storevar bv
        body:
            [[stmt]]
            atomic dec
        """

        # declare labels
        global labelcnt
        label_start = LabelValue(None, "LetWhenAST_start$%d" % labelcnt)
        labelcnt += 1
        label_condfailed = LabelValue(None, "LetWhenAST_condfailed$%d" % labelcnt)
        labelcnt += 1
        label_body = LabelValue(None, "LetWhenAST_body$%d" % labelcnt)
        labelcnt += 1

        # start:
        code.nextLabel(label_start)
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
            code.append(ReadonlyIncOp(), self.token, self.endtoken)
        ns = Scope(scope)
        for var_or_cond in self.vars_and_conds:
            if var_or_cond[0] == 'var':
                var, expr = var_or_cond[1:]
                expr.compile(ns, code)
                code.append(StoreVarOp(var), self.token, self.endtoken)
                self.define(ns, var)
            elif var_or_cond[0] == 'cond':
                cond = var_or_cond[1]
                cond.compile(ns, code)
                code.append(JumpCondOp(False, label_condfailed), self.token, self.endtoken)
            else:
                assert var_or_cond[0] == 'exists'
                (_, bv, expr) = var_or_cond
                (_, file, line, column) = self.token
                self.define(ns, bv)
                expr.compile(ns, code)
                code.append(DupOp(), self.token, self.endtoken)
                code.append(PushOp((SetValue(set()), file, line, column)), self.token, self.endtoken)
                code.append(NaryOp(("==", file, line, column), 2), self.token, self.endtoken)
                label_select = LabelValue(None, "LetWhenAST_select$%d" % labelcnt)
                labelcnt += 1
                code.append(JumpCondOp(False, label_select), self.token, self.endtoken)

                # set is empty.  Try again
                code.append(PopOp(), self.token, self.endtoken)
                if self.atomically:
                    code.append(ReadonlyDecOp(), self.token, self.endtoken)
                    code.append(AtomicDecOp(), self.token, self.endtoken)
                code.append(JumpOp(label_start), self.endtoken, self.endtoken)

                # select:
                code.nextLabel(label_select)
                code.append(ChooseOp(), self.token, self.endtoken)
                code.append(StoreVarOp(bv), self.token, self.endtoken)
        code.append(JumpOp(label_body), self.endtoken, self.endtoken)

        # condfailed:
        code.nextLabel(label_condfailed)
        if self.atomically:
            code.append(ReadonlyDecOp(), self.token, self.endtoken)
            code.append(AtomicDecOp(), self.token, self.endtoken)
        code.append(JumpOp(label_start), self.endtoken, self.endtoken)

        # body:
        code.nextLabel(label_body)
        if self.atomically:
            code.append(ReadonlyDecOp(), self.token, self.endtoken)
        self.stat.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def getLabels(self):
        return self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_let_when(self, *args, **kwargs)


class AtomicAST(AST):
    def __init__(self, endtoken, token, atomically, stat):
        AST.__init__(self, endtoken, token, atomically)
        self.stat = stat

    def __repr__(self):
        return "Atomic(" + str(self.stat) + ")"

    def compile(self, scope, code):
        code.append(AtomicIncOp(True), self.token, self.endtoken)
        self.stat.compile(scope, code)
        code.append(AtomicDecOp(), self.token, self.endtoken)

    # TODO.  Is it ok to define labels within an atomic block?
    def getLabels(self):
        return self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_atomic(self, *args, **kwargs)


class AssertAST(AST):
    def __init__(self, endtoken, token, atomically, cond, expr):
        AST.__init__(self, endtoken, token, atomically)
        self.cond = cond
        self.expr = expr

    def __repr__(self):
        return "Assert(" + str(self.token) + ", " + str(self.cond) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        code.append(ReadonlyIncOp(), self.token, self.endtoken)
        code.append(AtomicIncOp(True), self.token, self.endtoken)
        self.cond.compile(scope, code)
        if self.expr != None:
            self.expr.compile(scope, code)
        code.append(AssertOp(self.token, self.expr != None), self.token, self.endtoken)
        code.append(AtomicDecOp(), self.token, self.endtoken)
        code.append(ReadonlyDecOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_assert(self, *args, **kwargs)


class PrintAST(AST):
    def __init__(self, endtoken, token, atomically, expr):
        AST.__init__(self, endtoken, token, atomically)
        self.expr = expr

    def __repr__(self):
        return "Print(" + str(self.token) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        self.expr.compile(scope, code)
        code.append(PrintOp(self.token), self.token, self.endtoken)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_print(self, *args, **kwargs)


class MethodAST(AST):
    def __init__(self, endtoken, token, atomically, name, args, stat):
        AST.__init__(self, endtoken, token, atomically)
        self.name = name
        self.args = args
        self.stat = stat
        (lexeme, file, line, column) = name
        self.label = LabelValue(None, lexeme)

    def __repr__(self):
        return "Method(" + str(self.name) + ", " + str(self.args) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        global labelcnt
        endlabel = LabelValue(None, "$%d" % labelcnt)
        labelcnt += 1
        (lexeme, file, line, column) = self.name
        code.append(JumpOp(endlabel), self.token, self.token)
        code.nextLabel(self.label)
        code.append(FrameOp(self.name, self.args), self.token, self.endtoken)
        # scope.names[lexeme] = ("constant", (self.label, file, line, column))

        ns = Scope(scope)
        for ((lexeme, file, line, column), lb) in self.stat.getLabels():
            ns.names[lexeme] = ("constant", (lb, file, line, column))
        self.define(ns, self.args)
        ns.names["result"] = ("local-var", ("result", file, line, column))
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        self.stat.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)
        code.append(ReturnOp(), self.token, self.endtoken)
        code.nextLabel(endlabel)

        # promote global variables
        for name, (t, v) in ns.names.items():
            if t == "global" and name not in scope.names:
                scope.names[name] = (t, v)

    def getLabels(self):
        return {(self.name, self.label)} | self.stat.getLabels()

    def getImports(self):
        return self.stat.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_method(self, *args, **kwargs)


class LambdaAST(AST):
    def __init__(self, endtoken, args, stat, token, atomically):
        AST.__init__(self, endtoken, token, atomically)
        self.args = args
        self.stat = stat

    def __repr__(self):
        return "Lambda " + str(self.args) + ", " + str(self.stat) + ")"

    def isConstant(self, scope):
        return True

    def compile_body(self, scope, code):
        startlabel = LabelValue(None, "lambda")
        endlabel = LabelValue(None, "lambda")
        code.append(JumpOp(endlabel), self.token, self.token)
        code.nextLabel(startlabel)
        code.append(FrameOp(self.token, self.args), self.token, self.endtoken)

        (lexeme, file, line, column) = self.token
        ns = Scope(scope)
        self.define(ns, self.args)
        R = ("result", file, line, column)
        ns.names["result"] = ("local-var", R)
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        self.stat.compile(ns, code)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)
        code.append(StoreVarOp(R), self.token, self.endtoken)
        code.append(ReturnOp(), self.token, self.endtoken)
        code.nextLabel(endlabel)
        return startlabel

    def compile(self, scope, code):
        startlabel = self.compile_body(scope, code)
        (lexeme, file, line, column) = self.token
        code.append(PushOp((startlabel, file, line, column)), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_lambda(self, *args, **kwargs)


class CallAST(AST):
    def __init__(self, endtoken, token, atomically, expr):
        AST.__init__(self, endtoken, token, atomically)
        self.expr = expr

    def __repr__(self):
        return "Call(" + str(self.expr) + ")"

    def compile(self, scope, code):
        if not self.expr.isConstant(scope):
            if self.atomically:
                code.append(AtomicIncOp(True), self.token, self.endtoken)
            self.expr.compile(scope, code)
            if self.atomically:
                code.append(AtomicDecOp(), self.token, self.endtoken)
            code.append(PopOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_call(self, *args, **kwargs)


class SpawnAST(AST):
    def __init__(self, endtoken, token, atomically, method, arg, this, eternal):
        AST.__init__(self, endtoken, token, atomically)
        self.method = method
        self.arg = arg
        self.this = this
        self.eternal = eternal

    def __repr__(self):
        return "Spawn(" + str(self.method) + ", " + str(self.arg) + ", " + str(self.this) + ", " + str(
            self.eternal) + ")"

    def compile(self, scope, code):
        self.method.compile(scope, code)
        self.arg.compile(scope, code)
        if self.this == None:
            code.append(PushOp((emptydict, None, None, None)), self.token, self.endtoken)
        else:
            self.this.compile(scope, code)
        code.append(SpawnOp(self.eternal), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_spawn(self, *args, **kwargs)


class TrapAST(AST):
    def __init__(self, endtoken, token, atomically, method, arg):
        AST.__init__(self, endtoken, token, atomically)
        self.method = method
        self.arg = arg

    def __repr__(self):
        return "Trap(" + str(self.method) + ", " + str(self.arg) + ")"

    def compile(self, scope, code):
        # TODO.  These should be swapped
        self.arg.compile(scope, code)
        self.method.compile(scope, code)
        code.append(TrapOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_trap(self, *args, **kwargs)


class GoAST(AST):
    def __init__(self, endtoken, token, atomically, ctx, result):
        AST.__init__(self, endtoken, token, atomically)
        self.ctx = ctx
        self.result = result

    def __repr__(self):
        return "Go(" + str(self.ctx) + ", " + str(self.result) + ")"

    # TODO.  Seems like context and argument are not evaluated in left to
    #        right order
    def compile(self, scope, code):
        if self.atomically:
            code.append(AtomicIncOp(True), self.token, self.endtoken)
        self.result.compile(scope, code)
        self.ctx.compile(scope, code)
        if self.atomically:
            code.append(AtomicDecOp(), self.token, self.endtoken)
        code.append(GoOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_go(self, *args, **kwargs)


class ImportAST(AST):
    def __init__(self, endtoken, token, atomically, modlist):
        AST.__init__(self, endtoken, token, atomically)
        self.modlist = modlist

    def __repr__(self):
        return "Import(" + str(self.modlist) + ")"

    def compile(self, scope, code):
        for module in self.modlist:
            self.doImport(scope, code, module)

    def getImports(self):
        return self.modlist

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_import(self, *args, **kwargs)


class FromAST(AST):
    def __init__(self, endtoken, token, atomically, module, items):
        AST.__init__(self, endtoken, token, atomically)
        self.module = module
        self.items = items

    def __repr__(self):
        return "FromImport(" + str(self.module) + ", " + str(self.items) + ")"

    def compile(self, scope, code):
        self.doImport(scope, code, self.module)
        (lexeme, file, line, column) = self.module
        names = imported[lexeme].names
        # TODO.  Check for overlap, existence, etc.
        if self.items == []:  # from module import *
            for (item, (t, v)) in names.items():
                if t == "constant":
                    scope.names[item] = (t, v)
        else:
            for (lexeme, file, line, column) in self.items:
                if lexeme not in names:
                    raise HarmonyCompilerError(
                        filename=file,
                        lexeme=lexeme,
                        message="%s line %s: can't import %s from %s" % (file, line, lexeme, self.module[0]),
                        line=line, column=column)
                (t, v) = names[lexeme]
                assert t == "constant", (lexeme, t, v)
                scope.names[lexeme] = (t, v)

    def getImports(self):
        return [self.module]

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_from(self, *args, **kwargs)


class LocationAST(AST):
    def __init__(self, endtoken, token, ast, file, line):
        AST.__init__(self, endtoken, token, True)
        self.ast = ast
        self.file = file
        self.line = line

    def __repr__(self):
        return "LocationAST(" + str(self.ast) + ")"

    def compile(self, scope, code):
        code.location(self.file, self.line)
        self.ast.compile(scope, code)

    def getLabels(self):
        return self.ast.getLabels()

    def getImports(self):
        return self.ast.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_location(self, *args, **kwargs)


class LabelStatAST(AST):
    def __init__(self, endtoken, token, labels, ast):
        AST.__init__(self, endtoken, token, True)
        self.labels = {lb: LabelValue(None, lb[0]) for lb in labels}
        self.ast = ast

    def __repr__(self):
        return "LabelStatAST(" + str(self.labels) + ", " + str(self.ast) + ")"

    # TODO.  Update label stuff
    def compile(self, scope, code):
        # root = scope
        # while root.parent != None:
        #     root = root.parent
        for ((lexeme, file, line, column), label) in self.labels.items():
            code.nextLabel(label)
            # root.names[lexeme] = ("constant", (label, file, line, column))
        code.append(AtomicIncOp(False), self.token, self.endtoken)
        self.ast.compile(scope, code)
        code.append(AtomicDecOp(), self.token, self.endtoken)

    def getLabels(self):
        return set(self.labels.items()) | self.ast.getLabels()

    def getImports(self):
        return self.ast.getImports()

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_label_stat(self, *args, **kwargs)


class SequentialAST(AST):
    def __init__(self, endtoken, token, atomically, vars):
        AST.__init__(self, endtoken, token, atomically)
        self.vars = vars

    def __repr__(self):
        return "Sequential(" + str(self.vars) + ")"

    def compile(self, scope, code):
        for lv in self.vars:
            lv.ph1(scope, code)
            code.append(SequentialOp(), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_sequential(self, *args, **kwargs)


class BuiltinAST(AST):
    def __init__(self, endtoken, token, name, value):
        AST.__init__(self, endtoken, token, False)
        self.name = name
        self.value = value

    def __repr__(self):
        return "Builtin(" + str(self.name) + ", " + self.value + ")"

    def compile(self, scope, code):
        self.name.compile(scope, code)
        code.append(BuiltinOp(self.value), self.token, self.endtoken)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_builtin(self, *args, **kwargs)


class ConstAST(AST):
    def __init__(self, endtoken, token, atomically, const, expr):
        AST.__init__(self, endtoken, token, atomically)
        self.const = const
        self.expr = expr

    def __repr__(self):
        return "Const(" + str(self.const) + ", " + str(self.expr) + ")"

    def set(self, scope, const, v):
        if isinstance(const, tuple):
            (lexeme, file, line, column) = const
            if lexeme in scope.names:
                raise HarmonyCompilerError(
                    filename=file,
                    lexeme=lexeme,
                    line=line,
                    column=column,
                    message="%s: Parse error: already defined" % lexeme
                )
            if lexeme in constants:
                value = constants[lexeme]
                used_constants.add(lexeme)
            else:
                value = v
            scope.names[lexeme] = ("constant", (value, file, line, column))
        else:
            assert isinstance(const, list), const
            assert isinstance(v, ListValue), v
            assert len(const) == len(v.vals), (const, v)
            for i in range(len(const)):
                self.set(scope, const[i], v.vals[i])

    def compile(self, scope, code):
        if not self.expr.isConstant(scope):
            lexeme, file, line, column = self.expr.token if isinstance(self.expr, AST) else self.token
            raise HarmonyCompilerError(
                filename=file,
                lexeme=lexeme,
                line=line,
                column=column,
                message="%s: Parse error: expression not a constant %s" % (self.const, self.expr),
            )
        if isinstance(self.expr, LambdaAST):
            pc = self.expr.compile_body(scope, code)
            self.set(scope, self.const, PcValue(pc))
        else:
            code2 = Code()
            self.expr.compile(scope, code2)
            state = State(code2, scope.labels)
            ctx = ContextValue(("__const__", None, None, None), 0, emptytuple, emptydict)
            ctx.atomic = 1
            while ctx.pc != len(code2.labeled_ops):
                code2.labeled_ops[ctx.pc].op.eval(state, ctx)
            v = ctx.pop()
            self.set(scope, self.const, v)

    def accept_visitor(self, visitor, *args, **kwargs):
        return visitor.visit_const(self, *args, **kwargs)

