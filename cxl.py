import sys
import traceback
import collections

def islower(c):
    return c in "abcdefghijklmnopqrstuvwxyz"

def isupper(c):
    return c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def isletter(c):
    return islower(c) or isupper(c)

def isnumeral(c):
    return c in "0123456789"

def isalnum(c):
    return isletter(c) or isnumeral(c)

def isnamechar(c):
    return isalnum(c) or c == "_"

def isprint(c):
    return isinstance(c, str) and len(c) == 1 and (
        isalnum(c) or c in " ~`!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?")

def isnumber(s):
    return all(isnumeral(c) for c in s)

def isreserved(s):
    return s in [
        "assert",
        "atomic",
        "call",
        "choose",
        "const",
        "else",
        "end",
        "False",
        "if",
        "in",
        "not",
        "method",
        "skip",
        "spawn",
        "True",
        "var",
        "while"
    ]

def isname(s):
    return (not isreserved(s)) and (isletter(s[0]) or s[0] == "_") and \
                    all(isnamechar(c) for c in s)

def isunaryop(s):
    return s in [ "-", "not" ]

def isbinaryop(s):
    return s in [
            "==", "!=", "..",
            "-", "+", "*", "/", "%",
            "<", "<=", ">", ">=",
            "/\\", "and", "\\/", "or"
    ];

tokens = [ "dict{", ":=", "==", "!=", "<=", ">=", "..", "/\\", "\\/",
            "&(", "!(", "choose(" ]

def lexer(s, file):
    result = []
    line = 1
    column = 1
    while s != "":
        # see if it's a blank
        if s[0] in { " ", "\t" }:
            s = s[1:]
            column += 1
            continue

        if s[0] == "\n":
            s = s[1:]
            line += 1
            column = 1
            continue

        # skip over line comments
        if s.startswith("#"):
            s = s[1:]
            while len(s) > 0 and s[0] != '\n':
                s = s[1:]
            continue

        # skip over nested comments
        if s.startswith("(*"):
            count = 1
            s = s[2:]
            column += 2
            while count != 0 and s != "":
                if s.startswith("(*"):
                    count += 1
                    s = s[2:]
                    column += 2
                elif s.startswith("*)"):
                    count -= 1
                    s = s[2:]
                    column += 2
                elif s[0] == "\n":
                    s = s[1:]
                    line += 1
                    column = 1
                else:
                    s = s[1:]
                    column += 1
            continue

        # see if it's a multi-character token.  Match with the longest one
        found = ""
        for t in tokens:
            if s.startswith(t) and len(t) > len(found):
                found = t
        if found != "":
            result += [ (found, file, line, column) ]
            s = s[len(found):]
            column += len(found)
            continue

        # see if a sequence of letters and numbers
        if isnamechar(s[0]):
            i = 0
            while i < len(s) and isnamechar(s[i]):
                i += 1
            result += [ (s[:i], file, line, column) ]
            s = s[i:]
            column += i
            continue

        # string
        if s[0] == '"':
            i = 1
            str = '"'
            while i < len(s) and s[i] != '"':
                if s[i] == '\\':
                    i += 1
                    if i == len(s):
                        break
                    if s[i] == '"':
                        str += '"'
                    elif s[i] == '\\':
                        str += '\\'
                    elif s[i] == 't':
                        str += '\t'
                    elif s[i] == 'n':
                        str += '\n'
                    elif s[i] == 'f':
                        str += '\f'
                    elif s[i] == 'r':
                        str += '\r'
                    else:
                        str += s[i]
                else:
                    str += s[i]
                i += 1
            if i < len(s):
                i += 1
            str += '"'
            result += [ (str, file, line, column) ]
            s = s[i:]
            column += i
            continue

        # everything else is a single character token
        result += [ (s[0], file, line, column) ]
        s = s[1:]
        column += 1
    return result

class Value:
    pass

class NoValue(Value):
    def __repr__(self):
        return "NoValue()"

    def __hash__(self):
        return 0

    def __eq__(self, other):
        return isinstance(other, NoValue)

class PcValue(Value):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "PC(" + str(self.pc) + ")"

    def __hash__(self):
        return self.pc.__hash__()

    def __eq__(self, other):
        return isinstance(other, PcValue) and other.pc == self.pc

class RecordValue(Value):
    def __init__(self, d):
        self.d = d

    def __repr__(self):
        return str(self.d)

    def __hash__(self):
        hash = 0
        for x in self.d.items():
            hash ^= x.__hash__()
        return hash

    # Two dictionaries are the same if they have the same (key, value) pairs
    def __eq__(self, other):
        if not isinstance(other, RecordValue):
            return False
        if len(self.d.keys()) != len(other.d.keys()):
            return False
        for (k, v) in self.d.items():
            if v != other.d.get(k):
                return False
        return True

    def __len__(self):
        return len(self.d.keys())

class NameValue(Value):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        if not isinstance(other, NameValue):
            return False
        return self.name == other.name

class SetValue(Value):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        return str(self.s)

    def __hash__(self):
        return frozenset(self.s).__hash__()

    def __eq__(self, other):
        if not isinstance(other, SetValue):
            return False
        return self.s == other.s

class AddressValue(Value):
    def __init__(self, indexes):
        self.indexes = indexes

    def __repr__(self):
        return "AV(" + str(self.indexes) + ")"

    def __hash__(self):
        hash = 0
        for x in self.indexes:
            hash ^= x.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, AddressValue):
            return False
        return self.indexes == other.indexes

class Op:
    pass

# Splits a non-empty set in an element and its remainder
# TODO.  The element should be deterministically chosen, like minimum
class SplitOp(Op):
    def __repr__(self):
        return "Split"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, SetValue)
        assert v.s != set()
        lst = list(v.s)
        context.push(lst[0])
        context.push(SetValue(set(lst[1:])))
        context.pc += 1

class LoadOp(Op):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "Load " + str(self.name)

    def eval(self, state, context):
        (lexeme, file, line, column) = self.name
        context.push(state.get(lexeme))
        context.pc += 1

class LoadVarOp(Op):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "LoadVar " + str(self.name)

    def eval(self, state, context):
        (lexeme, file, line, column) = self.name
        context.push(context.get(lexeme))
        context.pc += 1

class ConstantOp(Op):
    def __init__(self, constant):
        self.constant = constant

    def __repr__(self):
        return "Constant " + str(self.constant)

    def eval(self, state, context):
        (lexeme, file, line, column) = self.constant
        context.push(lexeme)
        context.pc += 1

class LabelOp(Op):
    def __init__(self, label):
        self.label = label

    def __repr__(self):
        return "Label " + str(self.label)

    def eval(self, state, context):
        context.pc += 1

class NameOp(Op):
    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return "Name " + str(self.name)

    def eval(self, state, context):
        context.push(AddressValue([self.name]))
        context.pc += 1

class StoreOp(Op):
    def __init__(self, n):
        self.n = n                  # #indexes

    def __repr__(self):
        return "Store " + str(self.n)

    def eval(self, state, context):
        indexes = []
        for i in range(self.n):
            indexes.append(context.pop())
        av = indexes[0]
        assert isinstance(av, AddressValue)
        state.set(av.indexes + indexes[1:], context.pop())
        context.pc += 1

class AddressOp(Op):
    def __init__(self, n):
        self.n = n          # #indexes in LValue

    def __repr__(self):
        return "Address " + str(self.n)

    def eval(self, state, context):
        indexes = []
        for i in range(self.n):
            indexes.append(context.pop())
        av = indexes[0]
        assert isinstance(av, AddressValue), av
        context.push(AddressValue(av.indexes + indexes[1:]))
        context.pc += 1

class StoreVarOp(Op):
    def __init__(self, v, n):
        self.v = v
        self.n = n

    def __repr__(self):
        return "StoreVar " + str(self.v) + " " + str(self.n)

    def eval(self, state, context):
        (lexeme, file, line, column) = self.v
        indexes = []
        for i in range(self.n):
            indexes.append(context.pop())
        context.set([lexeme] + indexes, context.pop())
        context.pc += 1

class PointerOp(Op):
    def __repr__(self):
        return "Pointer"

    def eval(self, state, context):
        av = context.pop()
        assert isinstance(av, AddressValue), av
        context.push(state.iget(av.indexes))
        context.pc += 1

class ChooseOp(Op):
    def __repr__(self):
        return "Choose"

class AssertOp(Op):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return "Assert"

    def eval(self, state, context):
        expr = context.pop()
        cond = context.pop()
        assert isinstance(cond, bool)
        if not cond:
            print("Assertion failed", self.token, expr)
            state.assertFailure = True
        else:
            context.pc += 1

class PopOp(Op):
    def __init__(self):
        pass

    def __repr__(self):
        return "Pop"

    def eval(self, state, context):
        context.pop()
        context.pc += 1

class MethodOp(Op):
    def __init__(self, name, endpc):
        self.name = name
        self.endpc = endpc      # points to return code

    def __repr__(self):
        return "Method " + str(self.name) + " " + str(self.endpc)

    def eval(self, state, context):
        context.pc = self.endpc + 1

class FrameOp(Op):
    def __init__(self, name, arg, end):
        self.name = name
        self.arg = arg
        self.end = end

    def __repr__(self):
        return "Frame " + str(self.name) + " " + str(self.arg) + " " + str(self.end)

    def eval(self, state, context):
        arg = context.pop()
        context.push(context.vars)
        if self.arg == None:
            context.vars = RecordValue({})
        else:
            context.vars = RecordValue({ self.arg: arg })
        context.pc += 1

class ReturnOp(Op):
    def __init__(self, arg):
        self.arg = arg

    def __repr__(self):
        return "Return"

    def eval(self, state, context):
        if self.arg == None:
            result = NoValue()
        else:
            result = context.get(self.arg)
        context.vars = context.pop()
        context.pc = context.pop()
        context.push(result)

class SpawnOp(Op):
    def __init__(self, method, pc):
        self.method = method
        self.pc = pc

    def __repr__(self):
        return "Spawn " + str(self.pc)

    def eval(self, state, context):
        arg = context.pop()
        tag = context.pop()
        frame = state.code[self.pc]
        assert isinstance(frame, FrameOp)
        (lexeme, file, line, column) = self.method
        ctx = Context(lexeme, tag, self.pc, frame.end)
        ctx.push(arg)
        state.add(ctx)
        context.pc += 1

class AtomicIncOp(Op):
    def __repr__(self):
        return "AtomicInc"

    def eval(self, state, context):
        context.atomic += 1
        context.pc += 1

class AtomicDecOp(Op):
    def __repr__(self):
        return "AtomicDec"

    def eval(self, state, context):
        context.atomic -= 1
        context.pc += 1

class JumpOp(Op):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "Jump " + str(self.pc)

    def eval(self, state, context):
        context.pc = self.pc

class JumpFalseOp(Op):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "JumpFalse " + str(self.pc)

    def eval(self, state, context):
        c = context.pop()
        assert isinstance(c, bool), c
        if c:
            context.pc += 1
        else:
            context.pc = self.pc

class SetOp(Op):
    def __init__(self, nitems):
        self.nitems = nitems

    def __repr__(self):
        return "Set " + str(self.nitems)

    def eval(self, state, context):
        s = set()
        for i in range(self.nitems):
            s.add(context.pop())
        context.push(SetValue(s))
        context.pc += 1

class RecordOp(Op):
    def __repr__(self):
        return "Record"

    def eval(self, state, context):
        nitems = context.pop()
        d = {}
        for i in range(nitems):
            k = context.pop()
            v = context.pop()
            d[k] = v
        context.push(RecordValue(d))
        context.pc += 1

class TupleOp(Op):
    def __init__(self, nitems):
        self.nitems = nitems

    def __repr__(self):
        return "Tuple " + str(self.nitems)

    def eval(self, state, context):
        t = []
        for i in range(self.nitems):
            t.append(context.pop())
        context.push(tuple(t))
        context.pc += 1

class NaryOp(Op):
    def __init__(self, op, n):
        self.op = op
        self.n = n

    def __repr__(self):
        return "Nary " + str(self.op) + " " + str(self.n)

    def eval(self, state, context):
        (op, file, line, column) = self.op
        if self.n == 1:
            e = context.pop()
            if op == "-":
                assert isinstance(e, int)
                context.push(-e)
            elif op == "not":
                assert isinstance(e, bool)
                context.push(not e)
            elif op == "setsize":
                assert isinstance(e, SetValue)
                context.push(len(e.s))
            else:
                assert False, self
        elif self.n == 2:
            e1 = context.pop()
            e2 = context.pop()
            if op == "==":
                context.push(e1 == e2)
            elif op == "!=":
                context.push(e1 != e2)
            elif op == "+":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 + e2)
            elif op == "-":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 - e2)
            elif op == "*":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 * e2)
            elif op == "/":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 // e2)
            elif op == "%":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 % e2)
            elif op == "<":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 < e2)
            elif op == "<=":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 <= e2)
            elif op == ">":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 > e2)
            elif op == ">=":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(e1 >= e2)
            elif op == "..":
                assert isinstance(e1, int), e1
                assert isinstance(e2, int), e2
                context.push(SetValue(set(range(e1, e2+1))))
            elif op == "/\\" or op == "and":
                assert isinstance(e1, bool), e1
                assert isinstance(e2, bool), e2
                context.push(e1 and e2)
            elif op == "\\/" or op == "or":
                assert isinstance(e1, bool), e1
                assert isinstance(e2, bool), e2
                context.push(e1 or e2)
            else:
                assert False, self
        else:
            assert False, self
        context.pc += 1

class ApplyOp(Op):
    def __init__(self):
        pass

    def __repr__(self):
        return "Apply"

    def eval(self, state, context):
        method = context.pop()
        e = context.pop()
        if isinstance(method, RecordValue):
            context.push(method.d[e])
            context.pc += 1
        else:
            assert isinstance(method, PcValue), method
            context.push(context.pc + 1)
            context.push(e)
            context.pc = method.pc

class SetExpandOp(Op):
    def __repr__(self):
        return "SetExpand"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, SetValue)
        for e in v.s:
            context.push(e)
        context.push(len(v.s))
        context.pc += 1

class TupleExpandOp(Op):
    def __repr__(self):
        return "TupleExpand"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, tuple)
        n = len(v)
        for i in range(n):
            context.push(v[n - i - 1])
        context.push(n)
        context.pc += 1

class IterOp(Op):
    def __init__(self, method, pc):
        self.method = method
        self.pc = pc

    def __repr__(self):
        return "Iter " + str(self.method) + " " + str(self.pc)

    def eval(self, state, context):
        cnt = context.pop()
        if cnt > 0:
            v = context.pop()
            context.push(cnt - 1)
            context.push(context.pc + 1)
            context.push(v)
            context.pc = self.method
        else:
            context.pc = self.pc

class AST:
    pass

class ConstantAST(AST):
    def __init__(self, const):
        self.const = const

    def __repr__(self):
        return str(self.const)

    def compile(self, scope, code):
        code.append(ConstantOp(self.const))

class NameAST(AST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def compile(self, scope, code):
        tv = scope.lookup(self.name)
        if tv == None:
            code.append(LoadOp(self.name))
        else:
            (t, v) = tv
            if t == "variable":
                code.append(LoadVarOp(self.name))
            elif t == "constant":
                code.append(ConstantOp(v))
            elif t == "method":
                (lexeme, file, line, column) = self.name
                code.append(ConstantOp((PcValue(v), file, line, column)))
            else:
                assert False, tv

class SetAST(AST):
    def __init__(self, collection):
        self.collection = collection

    def __repr__(self):
        return str(self.collection)

    def compile(self, scope, code):
        for e in self.collection:
            e.compile(scope, code)
        code.append(SetOp(len(self.collection)))

class RecordAST(AST):
    def __init__(self, record):
        self.record = record

    def __repr__(self):
        return str(self.record)

    def compile(self, scope, code):
        for (k, v) in self.record.items():
            v.compile(scope, code)
            k.compile(scope, code)
        code.append(ConstantOp((len(self.record), None, None, None)))
        code.append(RecordOp())

class RecordComprehensionAST(AST):
    def __init__(self, key, value, arg, expr):
        self.key = key
        self.value = value
        self.arg = arg
        self.expr = expr

    def __repr__(self):
        return "RecordComprehension(" + str(self.arg) + ")"

    def compile(self, scope, code):
        (arg, file, line, column) = self.arg

        # TODO.  Figure out how to do this better
        ns = Scope(scope)
        ns.names[arg] = ("variable", self.arg)

        # Evaluate the set and store in a temporary variable
        # TODO.  Should store as sorted list for determinism
        self.expr.compile(ns, code)
        S = ("%set", file, line, column)
        code.append(StoreVarOp(S, 0))

        # Also store the size
        N = ("%size", file, line, column)
        code.append(LoadVarOp(S))
        code.append(NaryOp(("setsize", file, line, column), 1))
        code.append(StoreVarOp(N, 0))

        # Now generate the code:
        #   while X != {}:
        #       arg := oneof X
        #       X := X - arg
        #       push value
        #       push key
        pc = len(code)
        code.append(LoadVarOp(S))
        code.append(ConstantOp((SetValue(set()), file, line, column)))
        code.append(NaryOp(("!=", file, line, column), 2))
        tst = len(code)
        code.append(None)       # going to plug in a Jump op here
        code.append(LoadVarOp(S))
        code.append(SplitOp())  
        code.append(StoreVarOp(S, 0))
        code.append(StoreVarOp(self.arg, 0))
        self.value.compile(ns, code)
        self.key.compile(ns, code)
        code.append(JumpOp(pc))
        code[tst] = JumpFalseOp(len(code))
        code.append(LoadVarOp(N))
        code.append(RecordOp())

# N-ary operator
class NaryAST(AST):
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __repr__(self):
        return "NaryOp(" + str(self.op) + ", " + str(self.args) + ")"

    def compile(self, scope, code):
        n = len(self.args)
        for a in range(n):
            self.args[n - a - 1].compile(scope, code)
        code.append(NaryOp(self.op, n))

class ApplyAST(AST):
    def __init__(self, method, arg):
        self.method = method
        self.arg = arg

    def __repr__(self):
        return "Apply(" + str(self.method) + ", " + str(self.arg) + ")"

    def compile(self, scope, code):
        self.arg.compile(scope, code)
        self.method.compile(scope, code)
        code.append(ApplyOp())

class Rule:
    pass

class NaryRule(Rule):
    def __init__(self, closer):
        self.closer = closer

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if lexeme in { "-", "not" }:     # unary expression
            op = t[0]
            (ast, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == self.closer, t[0]
            return (NaryAST(op, [ast]), t[1:])
        # TODO.  Experimenting with an alternative syntax for "!()".
        #        But it doesn't work well for LValues
        if lexeme == "!":
            op = t[0]
            (ast, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == self.closer, t[0]
            return (PointerAST(ast), t[1:])
        (ast, t) = ExpressionRule().parse(t)
        (lexeme, file, line, column) = t[0]
        if lexeme == self.closer:
            return (ast, t[1:])
        op = t[0]
        assert isbinaryop(op[0]), op
        (ast2, t) = ExpressionRule().parse(t[1:])
        (lexeme, file, line, column) = t[0]
        assert lexeme == self.closer, (t[0], self.closer)
        return (NaryAST(op, [ast, ast2]), t[1:])

class RecordComprehensionRule(Rule):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def parse(self, t):
        name = t[0]
        (lexeme, file, line, column) = name
        assert isname(lexeme), name
        (lexeme, file, line, column) = t[1]
        assert lexeme == "in", t[1]
        (expr, t) = NaryRule("}").parse(t[2:])
        return (RecordComprehensionAST(self.key, self.value, name, expr), t)

class RecordRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        assert lexeme == "dict{", t[0]
        d = {}
        while lexeme != "}":
            (key, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ":", t[0]
            (value, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme in { ",", "}", "|" }, t[0]
            if lexeme == "|":
                assert d == {}, d
                return RecordComprehensionRule(key, value).parse(t[1:])
            d[key] = value
        return (RecordAST(d), t[1:])

class BasicExpressionRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if isnumber(lexeme):
            return (ConstantAST((int(lexeme), file, line, column)), t[1:])
        if lexeme == "False":
            return (ConstantAST((False, file, line, column)), t[1:])
        if lexeme == "True":
            return (ConstantAST((True, file, line, column)), t[1:])
        if isname(lexeme):
            return (NameAST(t[0]), t[1:])
        if lexeme[0] == '"':
            d = {}
            for i in range(1, len(lexeme) - 1):
                d[ConstantAST((i, file, line, column + i))] = \
                    ConstantAST((lexeme[i], file, line, column + i))
            return (RecordAST(d), t[1:])
        if lexeme == ".":
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            return (ConstantAST((lexeme, file, line, column)), t[2:])
        if lexeme == "{":
            s = set()
            while lexeme != "}":
                (next, t) = ExpressionRule().parse(t[1:])
                s.add(next)
                (lexeme, file, line, column) = t[0]
                assert lexeme in { ",", "}" }, t[0]
            return (SetAST(s), t[1:])
        if lexeme == "dict{":
            return RecordRule().parse(t)
        if lexeme == "(" or lexeme == "[":
            closer = ")" if lexeme == "(" else "]"
            (lexeme, file, line, column) = t[1]
            if lexeme == closer:
                return (ConstantAST(
                    (NoValue(), file, line, column)), t[2:])
            return NaryRule(closer).parse(t[1:])
        if lexeme == "&(":
            (ast, t) = LValueRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ")", t[0]
            return (AddressAST(ast), t[1:])
        if lexeme == "!(":
            (ast, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ")", t[0]
            return (PointerAST(ast), t[1:])
        if lexeme == "choose(":
            (ast, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ")", t[0]
            return (ChooseAST(ast), t[1:])
        return (False, t)

class LValueAST(AST):
    def __init__(self, indexes):
        self.indexes = indexes

    def __repr__(self):
        return "LValueRule(" + str(self.indexes) + ")"

class PointerAST(AST):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Pointer(" + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(PointerOp())

class ChooseAST(AST):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Choose(" + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(ChooseOp())

class ExpressionRule(Rule):
    def parse(self, t):
        (ast, t) = BasicExpressionRule().parse(t)
        while t != []:
            (arg, t) = BasicExpressionRule().parse(t)
            if arg == False:
                break
            (ast, t) = (ApplyAST(ast, arg), t)
        return (ast, t)

class AssignmentAST(AST):
    def __init__(self, lv, rv):
        self.lv = lv
        self.rv = rv

    def __repr__(self):
        return "Assign(" + str(self.lv) + ", " + str(self.rv) + ")"

    def compile(self, scope, code):
        self.rv.compile(scope, code)
        n = len(self.lv.indexes)
        for i in range(1, n):
            self.lv.indexes[n - i].compile(scope, code)
        lv = self.lv.indexes[0]
        if isinstance(lv, NameAST):
            tv = scope.lookup(lv.name)
            if tv == None:
                (lexeme, file, line, column) = lv.name
                code.append(NameOp(lexeme))
                code.append(StoreOp(n))
            else:
                (t, v) = tv
                if t == "variable":
                    code.append(StoreVarOp(v, n - 1))
                else:
                    assert False, tv
        else:
            assert isinstance(lv, PointerAST), lv
            lv.expr.compile(scope, code)
            code.append(StoreOp(n))

class AddressAST(AST):
    def __init__(self, lv):
        self.lv = lv

    def __repr__(self):
        return "Address(" + str(self.lv) + ")"

    def compile(self, scope, code):
        n = len(self.lv.indexes)
        for i in range(1, n):
            self.lv.indexes[n - i].compile(scope, code)
        lv = self.lv.indexes[0]
        if isinstance(lv, NameAST):
            tv = scope.lookup(lv.name)
            assert tv == None, tv   # can't take address of local var
            (lexeme, file, line, column) = lv.name
            code.append(NameOp(lexeme))
        else:
            assert isinstance(lv, PointerAST), lv
            lv.expr.compile(scope, code)
        code.append(AddressOp(n))

class SkipAST(AST):
    def __repr__(self):
        return "Skip"

    def compile(self, scope, code):
        pass

class BlockAST(AST):
    def __init__(self, b):
        self.b = b

    def __repr__(self):
        return "BlockRule(" + str(self.b) + ")"

    def compile(self, scope, code):
        for s in self.b:
            s.compile(scope, code)

class IfAST(AST):
    def __init__(self, alts, stat):
        self.alts = alts        # alternatives
        self.stat = stat        # else statement

    def __repr__(self):
        return "If(" + str(self.alts) + ", " + str(self.what) + ")"

    def compile(self, scope, code):
        jumps = []
        for alt in self.alts:
            (cond, stat) = alt
            cond.compile(scope, code)
            pc = len(code)
            code.append(None)
            stat.compile(scope, code)
            jumps += [len(code)]
            code.append(None)
            code[pc] = JumpFalseOp(len(code))
        if self.stat != None:
            self.stat.compile(scope, code)
        for pc in jumps:
            code[pc] = JumpOp(len(code))

class WhileAST(AST):
    def __init__(self, cond, stat):
        self.cond = cond
        self.stat = stat

    def __repr__(self):
        return "While(" + str(self.cond) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        pc1 = len(code)
        self.cond.compile(scope, code)
        pc2 = len(code)
        code.append(None)
        self.stat.compile(scope, code)
        code.append(JumpOp(pc1))
        code[pc2] = JumpFalseOp(len(code))

class AtomicAST(AST):
    def __init__(self, stat):
        self.stat = stat

    def __repr__(self):
        return "Atomic(" + str(self.stat) + ")"

    def compile(self, scope, code):
        code.append(AtomicIncOp())
        self.stat.compile(scope, code)
        code.append(AtomicDecOp())

class AssertAST(AST):
    def __init__(self, token, cond, expr):
        self.token = token
        self.cond = cond
        self.expr = expr

    def __repr__(self):
        return "Assert(" + str(self.token) + str(self.cond) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        self.cond.compile(scope, code)
        self.expr.compile(scope, code)
        code.append(AssertOp(self.token))

class MethodAST(AST):
    def __init__(self, name, arg, stat):
        self.name = name
        self.arg = arg
        self.stat = stat

    def __repr__(self):
        return "Method(" + str(self.name) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        pc = len(code)
        code.append(None)       # going to plug in a Jump op here
        ns = Scope(scope)
        if self.arg == None:
            arg = None
        else:
            (arg, file, line, column) = self.arg
            ns.names[arg] = ("variable", self.arg)
        code.append(None)
        self.stat.compile(ns, code)
        code.append(ReturnOp(arg))
        code[pc] = JumpOp(len(code))
        code[pc+1] = FrameOp(self.name, arg, len(code) - 1)
        (lexeme, file, line, column) = self.name
        scope.names[lexeme] = ("method", pc + 1)

class CallAST(AST):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Call(" + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(PopOp())

class SpawnAST(AST):
    def __init__(self, tag, method, expr):
        self.tag = tag
        self.method = method
        self.expr = expr

    def __repr__(self):
        return "Spawn(" + str(self.tag) + ", " + str(self.method) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        (t, v) = scope.lookup(self.method)
        assert t == "method"
        self.tag.compile(scope, code)
        self.expr.compile(scope, code)
        code.append(SpawnOp(self.method, v))

class LabelAST(AST):
    def __init__(self, label, ast):
        self.label = label
        self.ast = ast

    def __repr__(self):
        return "Label(" + str(self.label) + ", " + str(self.ast) + ")"

    def compile(self, scope, code):
        code.append(LabelOp(self.label))
        self.ast.compile(scope, code)

class VarAST(AST):
    def __init__(self, var, expr):
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "Var(" + str(self.var) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        (lexeme, file, line, column) = self.var
        scope.names[lexeme] = ("variable", self.var)
        code.append(StoreVarOp(self.var, 0))

class ConstAST(AST):
    def __init__(self, const, value):
        self.const = const
        self.value = value

    def __repr__(self):
        return "Const(" + str(self.const) + ", " + str(self.value) + ")"

    def compile(self, scope, code):
        (lexeme, file, line, column) = self.const
        scope.names[lexeme] = ("constant", self.value)

class LValueRule(Rule):
    def parse(self, t):
        (name, file, line, column) = t[0]
        if isname(name):
            indexes = [NameAST(t[0])]
        else:
            assert name == "!(", t[0]
            (ast, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ")"
            indexes = [PointerAST(ast)]
        t = t[1:]
        while t != []:
            (index, t) = BasicExpressionRule().parse(t)
            if index == False:
                break
            indexes.append(index)
        return (LValueAST(indexes), t)

class AssignmentRule(Rule):
    def parse(self, t):
        (lv, t) = LValueRule().parse(t)
        (lexeme, file, line, column) = t[0]
        assert lexeme == ":=", t[0]
        (rv, t) = NaryRule(";").parse(t[1:])
        return (AssignmentAST(lv, rv), t)

class StatListRule(Rule):
    def __init__(self, delim):
        self.delim = delim

    def parse(self, t):
        b = []
        (lexeme, file, line, column) = t[0]
        while lexeme not in self.delim:
            (ast, t) = StatementRule().parse(t)
            b.append(ast)
            if t == [] and self.delim == set():
                break
            (lexeme, file, line, column) = t[0]
        return (BlockAST(b), t)

class BlockRule(Rule):
    def __init__(self, delim):
        self.delim = delim

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        assert lexeme == ":", t[0]
        return StatListRule(self.delim).parse(t[1:])

class StatementRule(Rule):
    def parse(self, t):
        token = t[0]
        (lexeme, file, line, column) = token
        if lexeme == "@":
            label = t[1]
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            (lexeme, file, line, column) = t[2]
            assert lexeme == ":", t[2]
            (ast, t) = StatementRule().parse(t[3:])
            return (LabelAST(label, ast), t)
        if lexeme == "var":
            var = t[1]
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            (lexeme, file, line, column) = t[2]
            assert lexeme == "=", t[2]
            (ast, t) = NaryRule(";").parse(t[3:])
            return (VarAST(var, ast), t)
        if lexeme == "const":
            const = t[1]
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            (lexeme, file, line, column) = t[2]
            assert lexeme == "=", t[2]
            (ast, t) = NaryRule(";").parse(t[3:])
            assert isinstance(ast, ConstantAST), ast
            return (ConstAST(const, ast.const), t)
        if lexeme == "if":
            alts = []
            while True:
                (cond, t) = NaryRule(":").parse(t[1:])
                (stat, t) = StatListRule({ "else", "elif", "end" }).parse(t)
                alts += [(cond, stat)]
                (lexeme, file, line, column) = t[0]
                if lexeme in { "else", "end" }:
                    break
                assert lexeme == "elif", t[0]
                t = t[1:]
            if lexeme == "else":
                (stat, t) = BlockRule({"end"}).parse(t[1:])
                (lexeme, file, line, column) = t[0]
            else:
                stat = None
            assert lexeme == "end", t[0]
            (lexeme, file, line, column) = t[1]
            assert lexeme == "if", t[1]
            return (IfAST(alts, stat), t[2:])
        if lexeme == "while":
            (cond, t) = NaryRule(":").parse(t[1:])
            (stat, t) = StatListRule({"end"}).parse(t)
            (lexeme, file, line, column) = t[1]
            assert lexeme == "while", t[1]
            return (WhileAST(cond, stat), t[2:])
        if lexeme == "atomic":
            (stat, t) = BlockRule({"end"}).parse(t[1:])
            (lexeme, file, line, column) = t[1]
            assert lexeme == "atomic", t[1]
            return (AtomicAST(stat), t[2:])
        if lexeme == "def":
            name = t[1]
            (lexeme, file, line, column) = name
            assert isname(lexeme), name
            (lexeme, file, line, column) = t[2]
            assert lexeme == "(", t[2]
            arg = t[3]
            (lexeme, file, line, column) = arg
            if lexeme == ")":
                arg = None
                (stat, t) = BlockRule({"end"}).parse(t[4:])
            else:
                assert isname(lexeme), arg
                (lexeme, file, line, column) = t[4]
                assert lexeme == ")", t[4]
                (stat, t) = BlockRule({"end"}).parse(t[5:])
            (lexeme, file, line, column) = t[1]
            assert lexeme == "def", t[1]
            return (MethodAST(name, arg, stat), t[2:])
        if lexeme == "call":
            (expr, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ";", t[0]
            return (CallAST(expr), t[1:])
        if lexeme == "spawn":
            method = t[1]
            (lexeme, file, line, column) = method
            assert isname(lexeme), method
            (expr, t) = ExpressionRule().parse(t[2:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ",", t[0]
            (tag, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ";", t[0]
            return (SpawnAST(tag, method, expr), t[1:])
        if lexeme == "skip":
            return (SkipAST(), t[1:])
        if lexeme == "assert":
            (cond, t) = NaryRule(",").parse(t[1:])
            (expr, t) = NaryRule(";").parse(t)
            return (AssertAST(token, cond, expr), t)
        return AssignmentRule().parse(t)

class Context:
    def __init__(self, name, tag, pc, end):
        self.name = name
        self.tag = tag
        self.pc = pc
        self.end = end
        self.atomic = 0
        self.stack = []     # collections.deque() seems slightly slower
        self.vars = RecordValue({})

    def __repr__(self):
        return "Context(" + str(self.name) + ", " + str(self.tag) + ", " + str(self.pc) + ")"

    def __hash__(self):
        h = (self.name, self.tag, self.pc, self.end, self.atomic, self.vars).__hash__()
        for v in self.stack:
            h ^= v.__hash__()
        return h

    def __eq__(self, other):
        if not isinstance(other, Context):
            return False
        if self.name != other.name:
            return False
        if self.tag != other.tag:
            return False
        if self.pc != other.pc:
            return False
        if self.atomic != other.atomic:
            return False
        assert self.end == other.end
        return self.stack == other.stack and self.vars == other.vars

    def copy(self):
        c = Context(self.name, self.tag, self.pc, self.end)
        c.atomic = self.atomic
        c.stack = self.stack.copy()
        c.vars = self.vars
        return c

    def get(self, var):
        return self.vars.d[var]

    def iget(self, indexes):
        v = self.vars
        while indexes != []:
            v = v.d[indexes[0]]
            indexes = indexes[1:]
        return v

    def update(self, record, indexes, val):
        if len(indexes) > 1:
            v = self.update(record.d[indexes[0]], indexes[1:], val)
        else:
            v = val
        d = record.d.copy()
        d[indexes[0]] = v
        return RecordValue(d)

    def set(self, indexes, val):
        self.vars = self.update(self.vars, indexes, val)

    def push(self, val):
        assert val != None
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

class State:
    def __init__(self, code):
        self.code = code
        self.vars = RecordValue({})
        self.ctxbag = { Context("__main__", 0, 0, len(code)) : 1 }
        self.assertFailure = False

    def __repr__(self):
        return "State(" + str(self.vars) + ", " + str(self.ctxbag) + ")"

    def __hash__(self):
        h = self.vars.__hash__()
        for c in self.ctxbag.items():
            h ^= c.__hash__()
        return h

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        assert self.code == other.code
        if self.vars != other.vars:
            return False
        if self.ctxbag != other.ctxbag:
            return False
        if self.assertFailure != other.assertFailure:
            return False
        return True

    def copy(self):
        s = State(self.code)
        s.vars = self.vars      # no need to copy as store operations do it
        s.ctxbag = {}
        for (ctx, cnt) in self.ctxbag.items():
            s.ctxbag[ctx.copy()] = cnt     # TODO: can we avoid copy?
        s.assertFailure = self.assertFailure
        return s

    def get(self, var):
        return self.vars.d[var]

    def iget(self, indexes):
        v = self.vars
        while indexes != []:
            v = v.d[indexes[0]]
            indexes = indexes[1:]
        return v

    def update(self, record, indexes, val):
        if len(indexes) > 1:
            v = self.update(record.d[indexes[0]], indexes[1:], val)
        else:
            v = val
        d = record.d.copy()
        d[indexes[0]] = v
        return RecordValue(d)

    def set(self, indexes, val):
        self.vars = self.update(self.vars, indexes, val)

    def add(self, ctx):
        cnt = self.ctxbag.get(ctx)
        if cnt == None:
            self.ctxbag[ctx] = 1
        else:
            self.ctxbag[ctx] = cnt + 1

    def remove(self, ctx):
        cnt = self.ctxbag[ctx]
        assert cnt > 0
        if cnt == 1:
            del self.ctxbag[ctx]
        else:
            self.ctxbag[ctx] = cnt - 1

class Node:
    def __init__(self, parent, ctx, choice, steps, len):
        self.parent = parent
        self.ctx = ctx
        self.choice = choice
        self.steps = steps
        self.len = len
        self.edges = []

def print_path(visited, state):
    if state != None:
        node = visited[state]
        print_path(visited, node.parent)
        print(node.ctx, node.steps, state.vars)

def print_shortest(visited, bad):
    best_state = None
    best_len = 0
    for s in bad:
        node = visited[s]
        if best_state == None or node.len < best_len:
            best_state = s
            best_len = node.len
    print_path(visited, best_state)

class Scope:
    def __init__(self, parent):
        self.parent = parent
        self.names = {}

    def lookup(self, name):
        (lexeme, file, line, column) = name
        tv = self.names.get(lexeme)
        if tv != None:
            return tv
        ancestor = self.parent
        while ancestor != None:
            tv = ancestor.names.get(lexeme)
            if tv != None:
                (t, v) = tv
                # if t == "variable":
                #    return None
                return tv
            ancestor = ancestor.parent
        return None

# These operations cause global state changes
globops = [
    AtomicIncOp, LabelOp, LoadOp, SpawnOp, StoreOp
]

def onestep(state, ctx, choice, visited, todo, node, infloop):
    # Copy the state (TODO.  Should not have to copy contexts)
    sc = state.copy()

    # Remove context from bag
    sc.remove(ctx)

    # Make a copy of the context before modifying it.
    ctx = ctx.copy()

    if choice == None:
        steps = []
    else:
        steps = [ctx.pc]
        ctx.stack[-1] = choice
        ctx.pc += 1

    localStates = { ctx.copy() }
    foundInfLoop = False
    while not sc.assertFailure:
        # execute one step
        steps.append(ctx.pc)
        # print("PC", ctx.pc, sc.code[ctx.pc])
        sc.code[ctx.pc].eval(sc, ctx)

        # if we reached the end, remove the context
        if ctx.pc == ctx.end:
            break

        # if we're about to do a state change, let other processes
        # go first assuming there are other processes and we're not
        # in "atomic" mode
        if ctx.atomic == 0 and type(sc.code[ctx.pc]) in globops:
                            # TODO   and len(sc.ctxbag) > 1
            break
        if isinstance(sc.code[ctx.pc], ChooseOp):
            break

        # Detect infinite loops
        if ctx in localStates:
            foundInfLoop = True
            break
        localStates.add(ctx.copy())

    # Put the resulting context into the bag unless it's done
    if ctx.pc != ctx.end:
        sc.add(ctx)

    next = visited.get(sc)
    if next == None:
        next = Node(state, ctx, choice, steps, node.len + 1)
        visited[sc] = next
        todo.append(sc)
    node.edges.append(sc)

    if foundInfLoop:
        infloop.add(sc)

def optjump(code, pc):
    while pc < len(code):
        op = code[pc]
        if not isinstance(op, JumpOp):
            break
        pc = op.pc
    return pc

def optimize(code):
    for i in range(len(code)):
        op = code[i]
        if isinstance(op, JumpOp):
            code[i] = JumpOp(optjump(code, op.pc))
        elif isinstance(op, JumpFalseOp):
            code[i] = JumpFalseOp(optjump(code, op.pc))

def run(invariant, pcs):
    all = ""
    for line in sys.stdin:
       all += line
    tokens = lexer(all, "<stdin>")
    try:
        (ast, rem) = StatListRule(set()).parse(tokens)
    except IndexError as e:
        print("Parsing hit EOF (usually missing ';')?", e)
        print(traceback.format_exc())
        sys.exit(1)
    code = []
    ast.compile(Scope(None), code)

    optimize(code)

    for pc in range(len(code)):
        print(pc, code[pc])

    # Initial state
    state = State(code)

    # For traversing Kripke graph
    visited = { state: Node(None, None, None, None, 0) }
    todo = collections.deque([state])
    bad = set()
    infloop = set()

    cnt = 0
    while todo:
        cnt += 1
        state = todo.popleft()
        if state.assertFailure:
            bad.add(state)
            break
        node = visited[state]
        print(" ", cnt, "#states =", len(visited.keys()), "diameter =", node.len, "queue =", len(todo), end="     \r")

        if not invariant(state):
            bad.add(state)

        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc < ctx.end and isinstance(code[ctx.pc], ChooseOp):
                choices = ctx.stack[-1]
                assert isinstance(choices, SetValue), choices
                assert len(choices.s) > 0
                for choice in choices.s:
                    onestep(state, ctx, choice, visited, todo, node, infloop)
            else:
                onestep(state, ctx, None, visited, todo, node, infloop)
    print()

    # See if there has been a safety violation
    if len(bad) > 0:
        print("==== Safety violation ====")
        # TODO.  First one added to bad should have shortest path
        print_shortest(visited, bad)

    # See if there are processes stuck in infinite loops without accessing
    # shared state
    if len(infloop) > 0:
        print("==== Infinite Loop ====")
        print_shortest(visited, infloop)

    # See if there are livelocked states (states from which some process
    # cannot reach the reader or writer critical section)
    bad = set()
    for (p, cs) in pcs:
        # First collect all the states in which the process is in the
        # critical region
        good = set()
        for s in visited.keys():
            for ctx in s.ctxbag.keys():
                if (ctx.name, ctx.tag) == p:
                    op = s.code[ctx.pc]
                    if isinstance(op, LabelOp) and op.label[0] == cs:
                        good.add(s)
        progress = True
        while progress:
            progress = False
            for (s, node) in visited.items():
                if s not in good:
                    for reachable in node.edges:
                        if reachable in good:
                            progress = True
                            good.add(s)
                            break
        livelocked = set(visited.keys()).difference(good)
        bad = bad.union(livelocked)
    if len(bad) > 0:
        print("==== Livelock ====", len(bad))
        print_shortest(visited, bad)

    return visited
