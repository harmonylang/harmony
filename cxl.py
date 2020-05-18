import sys
import traceback
import collections

# TODO.  This should not be global ideally
files = {}

def load(f, filename, scope, code):
    files[filename] = []
    all = ""
    for line in f:
        files[filename] += [line]
        all += line
    tokens = lexer(all, filename)
    try:
        (ast, rem) = StatListRule(set()).parse(tokens)
    except IndexError as e:
        print("Parsing", filename, "hit EOF (usually missing ';' at end of last line)?", e)
        print(traceback.format_exc())
        sys.exit(1)
    ast.compile(scope, code)

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
        "and",
        "assert",
        "atLabel",
        "atomic",
        "call",
        "cardinality",
        "choose",
        "const",
        "def",
        "else",
        "False",
        "for",
        "if",
        "import",
        "in",
        "keys",
        "len",
        "nametag",
        "not",
        "or",
        "pass",
        "spawn",
        "True",
        "var",
        "while"
    ]

def isname(s):
    return (not isreserved(s)) and (isletter(s[0]) or s[0] == "_") and \
                    all(isnamechar(c) for c in s)

def isunaryop(s):
    return s in [ "^",
        # "-",
        "atLabel", "cardinality", "nametag", "not", "keys", "len" ]

def isbinaryop(s):
    return s in [
        "==", "!=", "..", "in", "and", "or",
        "-", "+", "*", "/", "%", "<", "<=", ">", ">="
    ];

tokens = [ "dict{", "==", "!=", "<=", ">=", "..", "&(", "choose(" ]

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

class PcValue(Value):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "PC(" + str(self.pc) + ")"

    def __hash__(self):
        return self.pc.__hash__()

    def __eq__(self, other):
        return isinstance(other, PcValue) and other.pc == self.pc

class OpValue(Value):
    def __init__(self, op):
        self.op = op

    def __repr__(self):
        return "Op(" + str(self.op) + ")"

    def __hash__(self):
        return self.op.__hash__()

    def __eq__(self, other):
        return isinstance(other, OpValue) and other.op == self.op

class DictValue(Value):
    def __init__(self, d):
        self.d = d

    def __repr__(self):
        if len(self.d) == 0:
            return "()"
        result = ""
        for (k, v) in self.d.items():
            if result != "":
                result += ", ";
            result += str(k) + ":" + str(v)
        return "dict{ " + result + " }"

    def __hash__(self):
        hash = 0
        for x in self.d.items():
            hash ^= x.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, DictValue):
            return False
        if len(self.d.keys()) != len(other.d.keys()):   # for efficiency
            return False
        return self.d == other.d

    def __len__(self):
        return len(self.d.keys())

# TODO.  Is there a better way than making this global?
novalue = DictValue({})

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

class NameOp(Op):
    def __init__(self, name):
        self.name = name 

    def __repr__(self):
        return "Name " + str(self.name)

    def eval(self, state, context):
        (lexeme, file, line, column) = self.name
        context.push(AddressValue([lexeme]))
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
        assert isinstance(av, AddressValue), indexes
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

class ChooseOp(Op):
    def __repr__(self):
        return "Choose"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, SetValue), v
        assert len(v.s) == 1, v
        for e in v.s:
            context.push(e)
        context.pc += 1

class AssertOp(Op):
    def __init__(self, token, exprthere):
        self.token = token
        self.exprthere = exprthere

    def __repr__(self):
        return "Assert"

    def eval(self, state, context):
        if self.exprthere:
            expr = context.pop()
        cond = context.pop()
        assert isinstance(cond, bool)
        if not cond:
            if self.exprthere:
                print("Assertion failed", self.token, expr)
            else:
                print("Assertion failed", self.token)
            state.failure = True
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
            context.vars = DictValue({ "result": novalue })
        else:
            (lexeme, file, line, column) = self.arg
            context.vars = DictValue({ "result": novalue, lexeme: arg })
        context.pc += 1

class ReturnOp(Op):
    def __repr__(self):
        return "Return"

    def eval(self, state, context):
        result = context.get("result")
        context.vars = context.pop()
        context.pc = context.pop()
        context.push(result)

class SpawnOp(Op):
    def __repr__(self):
        return "Spawn"

    def eval(self, state, context):
        method = context.pop()
        assert isinstance(method, PcValue)
        arg = context.pop()
        tag = context.pop()
        frame = state.code[method.pc]
        assert isinstance(frame, FrameOp)
        (lexeme, file, line, column) = frame.name
        ctx = Context(DictValue({"name": lexeme, "tag": tag}), method.pc, frame.end)
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

class JumpCondOp(Op):
    def __init__(self, cond, pc):
        self.cond = cond
        self.pc = pc

    def __repr__(self):
        return "JumpCond " + str(self.cond) + " " + str(self.pc)

    def eval(self, state, context):
        c = context.pop()
        assert isinstance(c, bool), c
        if c == self.cond:
            context.pc = self.pc
        else:
            context.pc += 1

class SetOp(Op):
    def __repr__(self):
        return "Set"

    def eval(self, state, context):
        nitems = context.pop()
        s = set()
        for i in range(nitems):
            s.add(context.pop())
        context.push(SetValue(s))
        context.pc += 1

class DictOp(Op):
    def __repr__(self):
        return "Dict"

    def eval(self, state, context):
        nitems = context.pop()
        d = {}
        for i in range(nitems):
            k = context.pop()
            v = context.pop()
            d[k] = v
        context.push(DictValue(d))
        context.pc += 1

class UnaryOp(Op):
    def __init__(self, op):
        self.op = op

    def __repr__(self):
        return "Unary " + str(self.op)

    def eval(self, state, context):
        (lexeme, file, line, column) = self.op
        context.push(OpValue(lexeme))
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
                assert isinstance(e, int), e
                context.push(-e)
            else:
                assert False, self
        elif self.n == 2:
            e1 = context.pop()
            e2 = context.pop()
            if op == "==":
                assert type(e1) == type(e2), (type(e1), type(e2))
                context.push(e1 == e2)
            elif op == "!=":
                assert type(e1) == type(e2), (type(e1), type(e2))
                context.push(e1 != e2)
            elif op == "+":
                if isinstance(e1, int):
                    assert isinstance(e2, int), e2
                    context.push(e1 + e2)
                else:
                    assert isinstance(e1, SetValue), e1
                    assert isinstance(e2, SetValue), e2
                    context.push(SetValue(e1.s.union(e2.s)))
            elif op == "-":
                if isinstance(e1, int):
                    assert isinstance(e2, int), e2
                    context.push(e1 - e2)
                else:
                    assert isinstance(e1, SetValue), e1
                    assert isinstance(e2, SetValue), e2
                    context.push(SetValue(e1.s.difference(e2.s)))
            elif op == "*":
                if isinstance(e1, int):
                    assert isinstance(e2, int), e2
                    context.push(e1 * e2)
                else:
                    assert isinstance(e1, SetValue), e1
                    assert isinstance(e2, SetValue), e2
                    context.push(SetValue(e1.s.intersection(e2.s)))
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
            elif op == "and":
                assert isinstance(e1, bool), e1
                assert isinstance(e2, bool), e2
                context.push(e1 and e2)
            elif op == "or":
                assert isinstance(e1, bool), e1
                assert isinstance(e2, bool), e2
                context.push(e1 or e2)
            elif op == "in":
                assert isinstance(e2, SetValue), e2
                context.push(e1 in e2.s)
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

    def atLabel(self, state, label):
        pc = state.labels[label]
        d = {}
        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc == pc:
                c = d.get(ctx.nametag)
                d[ctx.nametag] = 1 if c == None else (c + 1)
        return DictValue(d)

    def eval(self, state, context):
        method = context.pop()
        e = context.pop()
        if isinstance(method, DictValue):
            context.push(method.d[e])
            context.pc += 1
        elif isinstance(method, OpValue):
            op = method.op
            if op == "^":
                assert isinstance(e, AddressValue), e
                context.push(state.iget(e.indexes))
            elif op == "-":
                assert isinstance(e, int), e
                context.push(-e)
            elif op == "not":
                assert isinstance(e, bool), e
                context.push(not e)
            elif op == "atLabel":
                assert isinstance(e, str), e
                context.push(self.atLabel(state, e))
            elif op == "cardinality":
                assert isinstance(e, SetValue), e
                context.push(len(e.s))
            elif op == "nametag":
                assert isinstance(e, DictValue), e
                assert len(e) == 0
                context.push(context.nametag)
            elif op == "len":
                assert isinstance(e, DictValue), e
                context.push(len(e.d))
            elif op == "keys":
                assert isinstance(e, DictValue), e
                context.push(SetValue(set(e.d.keys())))
            else:
                assert False, self
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

class UnaryAST(AST):
    def __init__(self, op):
        self.op = op

    def __repr__(self):
        return str(self.op)

    def compile(self, scope, code):
        code.append(UnaryOp(self.op))

class NameAST(AST):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)

    def compile(self, scope, code):
        (lexeme, file, line, column) = self.name
        tv = scope.lookup(self.name)
        if tv == None:
            code.append(LoadOp(self.name))
        else:
            (t, v) = tv
            if t == "variable":
                code.append(LoadVarOp(self.name))
            elif t == "constant":
                code.append(ConstantOp(v))
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
        code.append(ConstantOp((len(self.collection), None, None, None)))
        code.append(SetOp())

class DictAST(AST):
    def __init__(self, record):
        self.record = record

    def __repr__(self):
        return str(self.record)

    def compile(self, scope, code):
        for (k, v) in self.record.items():
            v.compile(scope, code)
            k.compile(scope, code)
        code.append(ConstantOp((len(self.record), None, None, None)))
        code.append(DictOp())

class SetComprehensionAST(AST):
    def __init__(self, value, var, expr):
        self.value = value
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "SetComprehension(" + str(self.var) + ")"

    def compile(self, scope, code):
        (var, file, line, column) = self.var

        # Evaluate the set and store in a temporary variable
        # TODO.  Should store as sorted list for determinism
        self.expr.compile(scope, code)
        S = ("%set", file, line, column)
        code.append(StoreVarOp(S, 0))

        # Also store the size
        N = ("%size", file, line, column)
        code.append(LoadVarOp(S))
        code.append(UnaryOp(("cardinality", file, line, column)))
        code.append(ApplyOp())
        code.append(StoreVarOp(N, 0))

        # Now generate the code:
        #   while X != {}:
        #       var := oneof X
        #       X := X - var
        #       push value
        pc = len(code)
        code.append(LoadVarOp(S))
        code.append(ConstantOp((SetValue(set()), file, line, column)))
        code.append(NaryOp(("!=", file, line, column), 2))
        tst = len(code)
        code.append(None)       # going to plug in a Jump op here
        code.append(LoadVarOp(S))
        code.append(SplitOp())  
        code.append(StoreVarOp(S, 0))
        code.append(StoreVarOp(self.var, 0))

        # TODO.  Figure out how to do this better
        ns = Scope(scope)
        ns.names[var] = ("variable", self.var)

        self.value.compile(ns, code)
        code.append(JumpOp(pc))
        code[tst] = JumpCondOp(False, len(code))
        code.append(LoadVarOp(N))
        code.append(SetOp())

class DictComprehensionAST(AST):
    def __init__(self, value, var, expr):
        self.value = value
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "DictComprehension(" + str(self.var) + ")"

    def compile(self, scope, code):
        (var, file, line, column) = self.var

        # Evaluate the set and store in a temporary variable
        # TODO.  Should store as sorted list for determinism
        self.expr.compile(scope, code)
        S = ("%set", file, line, column)
        code.append(StoreVarOp(S, 0))

        # Also store the size
        N = ("%size", file, line, column)
        code.append(LoadVarOp(S))
        code.append(UnaryOp(("cardinality", file, line, column)))
        code.append(ApplyOp())
        code.append(StoreVarOp(N, 0))

        # Now generate the code:
        #   while X != {}:
        #       var := oneof X
        #       X := X - var
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
        code.append(StoreVarOp(self.var, 0))

        # TODO.  Figure out how to do this better
        ns = Scope(scope)
        ns.names[var] = ("variable", self.var)

        self.value.compile(ns, code)
        code.append(LoadVarOp(self.var))
        code.append(JumpOp(pc))
        code[tst] = JumpCondOp(False, len(code))
        code.append(LoadVarOp(N))
        code.append(DictOp())

class TupleComprehensionAST(AST):
    def __init__(self, value, var, expr):
        self.value = value
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "TupleComprehension(" + str(self.var) + ")"

    def compile(self, scope, code):
        (var, file, line, column) = self.var

        # Evaluate the set and store in a temporary variable
        # TODO.  Should store as sorted list for determinism
        self.expr.compile(scope, code)
        S = ("%set", file, line, column)
        code.append(StoreVarOp(S, 0))

        # Also store the size
        N = ("%size", file, line, column)
        code.append(LoadVarOp(S))
        code.append(UnaryOp(("cardinality", file, line, column)))
        code.append(ApplyOp())
        code.append(StoreVarOp(N, 0))

        # Create an index variable, initialized to 0
        code.append(ConstantOp((0, file, line, column)))
        I = ("%index", file, line, column)
        code.append(StoreVarOp(I, 0))

        # Now generate the code:
        #   while X != {}:
        #       var := oneof X
        #       X := X - var
        #       push value
        #       push index
        #       increment index
        pc = len(code)
        code.append(LoadVarOp(S))
        code.append(ConstantOp((SetValue(set()), file, line, column)))
        code.append(NaryOp(("!=", file, line, column), 2))
        tst = len(code)
        code.append(None)       # going to plug in a Jump op here
        code.append(LoadVarOp(S))
        code.append(SplitOp())  
        code.append(StoreVarOp(S, 0))
        code.append(StoreVarOp(self.var, 0))

        # TODO.  Figure out how to do this better
        ns = Scope(scope)
        ns.names[var] = ("variable", self.var)

        # push value and index
        self.value.compile(ns, code)
        code.append(LoadVarOp(I))

        # increment index
        code.append(ConstantOp((1, file, line, column)))
        code.append(LoadVarOp(I))
        code.append(NaryOp(("+", file, line, column), 2))
        code.append(StoreVarOp(I, 0))

        code.append(JumpOp(pc))
        code[tst] = JumpCondOp(False, len(code))
        code.append(LoadVarOp(N))
        code.append(DictOp())

# N-ary operator
class NaryAST(AST):
    def __init__(self, op, args):
        self.op = op
        self.args = args

    def __repr__(self):
        return "NaryOp(" + str(self.op) + ", " + str(self.args) + ")"

    def compile(self, scope, code):
        (op, file, line, column) = self.op
        n = len(self.args)
        if n == 2 and (op == "and" or op == "or"):
            self.args[0].compile(scope, code)
            code.append(JumpCondOp(op == "and", len(code) + 3))
            code.append(ConstantOp((op == "or", file, line, column)))
            pc = len(code)
            code.append(None)
            self.args[1].compile(scope, code)
            code[pc] = JumpOp(len(code))
        else:
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
    def __init__(self, closers):
        self.closers = closers

    def parse(self, t):
        (ast, t) = ExpressionRule().parse(t)
        (lexeme, file, line, column) = t[0]
        if lexeme in self.closers:
            return (ast, t)
        op = t[0]
        assert isbinaryop(op[0]), op
        (ast2, t) = ExpressionRule().parse(t[1:])
        (lexeme, file, line, column) = t[0]
        assert lexeme in self.closers, (t[0], self.closers)
        return (NaryAST(op, [ast, ast2]), t)

class SetComprehensionRule(Rule):
    def __init__(self, value):
        self.value = value

    def parse(self, t):
        name = t[0]
        (lexeme, file, line, column) = name
        assert isname(lexeme), name
        (lexeme, file, line, column) = t[1]
        assert lexeme == "in", t[1]
        (expr, t) = NaryRule({"}"}).parse(t[2:])
        return (SetComprehensionAST(self.value, name, expr), t[1:])

class DictComprehensionRule(Rule):
    def __init__(self, value):
        self.value = value

    def parse(self, t):
        name = t[0]
        (lexeme, file, line, column) = name
        assert isname(lexeme), name
        (lexeme, file, line, column) = t[1]
        assert lexeme == "in", t[1]
        (expr, t) = NaryRule({"}"}).parse(t[2:])
        return (DictComprehensionAST(self.value, name, expr), t[1:])

class TupleComprehensionRule(Rule):
    def __init__(self, ast, closer):
        self.ast = ast
        self.closer = closer

    def parse(self, t):
        name = t[0]
        (lexeme, file, line, column) = name
        assert isname(lexeme), name
        (lexeme, file, line, column) = t[1]
        assert lexeme == "in", t[1]
        (expr, t) = NaryRule({"]"}).parse(t[2:])
        return (TupleComprehensionAST(self.ast, name, expr), t[1:])

class SetRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        assert lexeme == "{", t[0]
        (lexeme, file, line, column) = t[1]
        if lexeme == "}":
            return (SetAST([]), t[2:])
        s = []
        while True:
            (next, t) = NaryRule({"for", ",", "}"}).parse(t[1:])
            s.append(next)
            (lexeme, file, line, column) = t[0]
            if lexeme == "for":
                assert len(s) == 1, s
                return SetComprehensionRule(s[0]).parse(t[1:])
            if lexeme == "}":
                return (SetAST(s), t[1:])
            assert lexeme == ",", t[0]

class DictRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        assert lexeme == "dict{", t[0]
        d = {}
        while lexeme != "}":
            (key, t) = NaryRule({":", "for"}).parse(t[1:])
            (lexeme, file, line, column) = t[0]
            if lexeme == "for":
                assert d == {}, d
                return DictComprehensionRule(key).parse(t[1:])
            assert lexeme == ":", t[0]
            (value, t) = NaryRule({",", "}"}).parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme in { ",", "}" }, t[0]
            d[key] = value
        return (DictAST(d), t[1:])

class TupleRule(Rule):
    def __init__(self, ast, closer):
        self.ast = ast
        self.closer = closer

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if lexeme == "for":
            return TupleComprehensionRule(self.ast, self.closer).parse(t[1:])
        d = { ConstantAST((0, file, line, column)): self.ast }
        i = 1
        while lexeme == ",":
            (next, t) = NaryRule({ self.closer, "," }).parse(t[1:])
            d[ConstantAST((i, file, line, column))] = next
            i += 1
            (lexeme, file, line, column) = t[0]
        assert lexeme == self.closer, t[0]
        return (DictAST(d), t[1:])

class BasicExpressionRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if isnumber(lexeme):
            return (ConstantAST((int(lexeme), file, line, column)), t[1:])
        if isunaryop(lexeme):
            return (UnaryAST(t[0]), t[1:])
        if lexeme == "False":
            return (ConstantAST((False, file, line, column)), t[1:])
        if lexeme == "True":
            return (ConstantAST((True, file, line, column)), t[1:])
        if lexeme[0] == '"':
            return (ConstantAST((lexeme[1:-1], file, line, column)), t[1:])
        if lexeme == ".":
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            return (ConstantAST((lexeme, file, line, column)), t[2:])
        if isname(lexeme):
            return (NameAST(t[0]), t[1:])
        if lexeme == "{":
            return SetRule().parse(t)
        if lexeme == "dict{":
            return DictRule().parse(t)
        if lexeme == "(" or lexeme == "[":
            closer = ")" if lexeme == "(" else "]"
            (lexeme, file, line, column) = t[1]
            if lexeme == closer:
                return (ConstantAST(
                    (novalue, file, line, column)), t[2:])
            (ast, t) = NaryRule({closer, ",", "for"}).parse(t[1:])
            (lexeme, file, line, column) = t[0]
            if lexeme != closer:
                return TupleRule(ast, closer).parse(t)
            else:
                return (ast, t[1:])
        if lexeme == "&(":
            (ast, t) = LValueRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ")", t[0]
            return (AddressAST(ast), t[1:])
        if lexeme == "choose(":
            (ast, t) = NaryRule({")"}).parse(t[1:])
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
        # Special treatment of unary minus
        (lexeme, file, line, column) = t[0]
        if lexeme == "-":
            (ast, t) = (UnaryAST(t[0]), t[1:])
        else:
            (ast, t) = BasicExpressionRule().parse(t)
        if t != []:
            (arg, t) = BasicExpressionRule().parse(t)
            if arg != False:
                return (ApplyAST(ast, arg), t)
        return (ast, t)

class AssignmentAST(AST):
    def __init__(self, lv, rv):
        self.lv = lv
        self.rv = rv

    def __repr__(self):
        return "Assign(" + str(self.lv) + ", " + str(self.rv) + ")"

    def compile(self, scope, code):
        self.rv.compile(scope, code)
        assert isinstance(self.lv, LValueAST)
        n = len(self.lv.indexes)
        for i in range(1, n):
            self.lv.indexes[n - i].compile(scope, code)
        lv = self.lv.indexes[0]
        if isinstance(lv, NameAST):
            tv = scope.lookup(lv.name)
            if tv == None:
                code.append(NameOp(lv.name))
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
            code.append(NameOp(lv.name))
        else:
            assert isinstance(lv, PointerAST), lv
            lv.expr.compile(scope, code)
        code.append(AddressOp(n))

class PassAST(AST):
    def __repr__(self):
        return "Pass"

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
            code[pc] = JumpCondOp(False, len(code))
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
        code[pc2] = JumpCondOp(False, len(code))

class ForAST(AST):
    def __init__(self, var, expr, stat):
        self.var = var
        self.expr = expr
        self.stat = stat

    def __repr__(self):
        return "For(" + str(self.var) + ", " + str(self.expr) + ", " + str(self.stat) + ")"

    def compile(self, scope, code):
        (var, file, line, column) = self.var

        self.expr.compile(scope, code)     # first push the set
        S = ("%set", file, line, column)   # save in variable "%set"
        code.append(StoreVarOp(S, 0))

        # Also store the size
        N = ("%size", file, line, column)
        code.append(LoadVarOp(S))
        code.append(UnaryOp(("cardinality", file, line, column)))
        code.append(ApplyOp())
        code.append(StoreVarOp(N, 0))

        pc = len(code)      # top of loop
        code.append(LoadVarOp(S))
        code.append(ConstantOp((SetValue(set()), file, line, column)))
        code.append(NaryOp(("!=", file, line, column), 2))
        tst = len(code)
        code.append(None)       # going to plug in a Jump op here
        code.append(LoadVarOp(S))
        code.append(SplitOp())  
        code.append(StoreVarOp(S, 0))
        code.append(StoreVarOp(self.var, 0))

        # TODO.  Figure out how to do this better
        ns = Scope(scope)
        ns.names[var] = ("variable", self.var)

        self.stat.compile(ns, code)
        code.append(JumpOp(pc))
        code[tst] = JumpCondOp(False, len(code))

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
        code.append(AtomicIncOp())
        self.cond.compile(scope, code)
        if self.expr != None:
            self.expr.compile(scope, code)
        code.append(AssertOp(self.token, self.expr != None))
        code.append(AtomicDecOp())

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
        code.append(None)       # going to plug in a Frame op here
        (lexeme, file, line, column) = self.name
        scope.names[lexeme] = ("constant", (PcValue(pc + 1), file, line, column))

        ns = Scope(scope)
        if self.arg == None:
            arg = None
        else:
            (arg, afile, aline, acolumn) = self.arg
            ns.names[arg] = ("variable", self.arg)
        ns.names["result"] = ("variable", ("result", file, line, column))
        self.stat.compile(ns, code)
        code.append(ReturnOp())

        code[pc+0] = JumpOp(len(code))
        code[pc+1] = FrameOp(self.name, self.arg, len(code) - 1)

class CallAST(AST):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Call(" + str(self.expr) + ")"

    def compile(self, scope, code):
        self.expr.compile(scope, code)
        code.append(PopOp())

class SpawnAST(AST):
    def __init__(self, tag, method, arg):
        self.tag = tag
        self.method = method
        self.arg = arg

    def __repr__(self):
        return "Spawn(" + str(self.tag) + ", " + str(self.method) + ", " + str(self.arg) + ")"

    def compile(self, scope, code):
        self.tag.compile(scope, code)
        self.arg.compile(scope, code)
        self.method.compile(scope, code)
        code.append(SpawnOp())

class ImportAST(AST):
    def __init__(self, module):
        self.module = module

    def __repr__(self):
        return "Import(" + str(self.module) + ")"

    def compile(self, scope, code):
        (lexeme, file, line, column) = self.module
        filename = lexeme + ".cxl"
        with open(filename) as f:
            load(f, filename, scope, code)

class LabelStatAST(AST):
    def __init__(self, labels, ast, file, line):
        self.labels = labels
        self.ast = ast
        self.file = file
        self.line = line

    def __repr__(self):
        return "LabelStat(" + str(self.labels) + ", " + str(self.ast) + ")"

    def compile(self, scope, code):
        scope.location(len(code), self.file, self.line, self.labels)
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
    def __init__(self, const, expr):
        self.const = const
        self.expr = expr

    def __repr__(self):
        return "Const(" + str(self.const) + ", " + str(self.expr) + ")"

    def compile(self, scope, code):
        code2 = []
        self.expr.compile(scope, code2)
        state = State(code2, scope.labels)
        contexts = list(state.ctxbag.keys())
        assert len(contexts) == 1
        ctx = contexts[0]
        while ctx.pc != len(code2):
            code2[ctx.pc].eval(state, ctx)
        v = ctx.pop()
        print("CONSTANT", self.const, v)
        (lexeme, file, line, column) = self.const
        scope.names[lexeme] = ("constant", (v, file, line, column))

class LValueRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if lexeme == "^":
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            return (LValueAST([PointerAST(NameAST(t[1]))]), t[2:])
        elif lexeme == "(":
            (lexeme, file, line, column) = t[1]
            (ast, t) = BasicExpressionRule().parse(t[2:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ")", t[0]
            indexes = [PointerAST(ast)]
            t = t[1:]
        else:
            assert isname(lexeme), t[0]
            indexes = [NameAST(t[0])]
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
        assert lexeme == "=", t[0]
        (rv, t) = NaryRule({";"}).parse(t[1:])
        return (AssignmentAST(lv, rv), t[1:])

# Zero or more labels, then a statement, then a semicolon
class LabelStatRule(Rule):
    def parse(self, t):
        (lexeme, thefile, theline, column) = t[0]
        labels = []
        while True:
            (lexeme, file, line, column) = t[0]
            if lexeme != "@":
                break
            label = t[1]
            (lexeme, file, line, column) = label
            assert isname(lexeme), t[1]
            labels.append(label)
            (lexeme, file, line, column) = t[2]
            assert lexeme == ":", t[2]
            t = t[3:]

        (ast, t) = StatementRule().parse(t)
        return (LabelStatAST(labels, ast, thefile, theline), t)

class StatListRule(Rule):
    def __init__(self, delim):
        self.delim = delim

    def parse(self, t):
        b = []
        (lexeme, file, line, column) = t[0]
        while lexeme not in self.delim:
            (ast, t) = LabelStatRule().parse(t)
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
    def skip(self, token, t):
        (lex2, file2, line2, col2) = t[0]
        assert lex2 == ";", t[0]
        (lex1, file1, line1, col1) = token
        if not ((line1 == line2) or (col1 == col2)):
            print("warning: ';' does not line up", token, t[0])
        return t[1:]
        
    def parse(self, t):
        token = t[0]
        (lexeme, file, line, column) = token
        if lexeme == "var":
            var = t[1]
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            (lexeme, file, line, column) = t[2]
            assert lexeme == "=", t[2]
            (ast, t) = NaryRule({";"}).parse(t[3:])
            return (VarAST(var, ast), self.skip(token, t))
        if lexeme == "const":
            const = t[1]
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            (lexeme, file, line, column) = t[2]
            assert lexeme == "=", t[2]
            (ast, t) = NaryRule({";"}).parse(t[3:])
            return (ConstAST(const, ast), self.skip(token, t))
        if lexeme == "if":
            alts = []
            while True:
                (cond, t) = NaryRule({":"}).parse(t[1:])
                (stat, t) = StatListRule({ "else", "elif", ";" }).parse(t[1:])
                alts += [(cond, stat)]
                (lexeme, file, line, column) = t[0]
                if lexeme in { "else", ";" }:
                    break
                assert lexeme == "elif", t[0]
            if lexeme == "else":
                (stat, t) = BlockRule({";"}).parse(t[1:])
            else:
                stat = None
            return (IfAST(alts, stat), self.skip(token, t))
        if lexeme == "while":
            (cond, t) = NaryRule({":"}).parse(t[1:])
            (stat, t) = StatListRule({";"}).parse(t[1:])
            return (WhileAST(cond, stat), self.skip(token, t))
        if lexeme == "for":
            var = t[1]
            (lexeme, file, line, column) = var
            assert isname(lexeme), var
            (lexeme, file, line, column) = t[2]
            assert lexeme == "in", t[2]
            (s, t) = NaryRule({":"}).parse(t[3:])
            (stat, t) = StatListRule({";"}).parse(t[1:])
            return (ForAST(var, s, stat), self.skip(token, t))
        if lexeme == "atomic":
            (stat, t) = BlockRule({";"}).parse(t[1:])
            return (AtomicAST(stat), self.skip(token, t))
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
                (stat, t) = BlockRule({";"}).parse(t[4:])
            else:
                assert isname(lexeme), arg
                (lexeme, file, line, column) = t[4]
                assert lexeme == ")", t[4]
                (stat, t) = BlockRule({";"}).parse(t[5:])
            return (MethodAST(name, arg, stat), self.skip(token, t))
        if lexeme == "call":
            (expr, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ";", t[0]
            return (CallAST(expr), self.skip(token, t))
        if lexeme == "spawn":
            (method, t) = BasicExpressionRule().parse(t[1:])
            (arg, t) = BasicExpressionRule().parse(t)
            (lexeme, file, line, column) = t[0]
            assert lexeme == ",", t[0]
            (tag, t) = NaryRule({";"}).parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ";", t[0]
            return (SpawnAST(tag, method, arg), self.skip(token, t))
        if lexeme == "pass":
            return (PassAST(), self.skip(token, t[1:]))
        if lexeme == "import":
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            return (ImportAST(t[1]), self.skip(token, t[2:]))
        if lexeme == "assert":
            (cond, t) = NaryRule({",", ";"}).parse(t[1:])
            (lexeme, file, line, column) = t[0]
            if lexeme == ",":
                (expr, t) = NaryRule({";"}).parse(t[1:])
            else:
                assert lexeme == ";", t[0]
                expr = None
            return (AssertAST(token, cond, expr), self.skip(token, t))
        return AssignmentRule().parse(t)

class Context:
    def __init__(self, nametag, pc, end):
        self.nametag = nametag
        self.pc = pc
        self.end = end
        self.atomic = 0
        self.stack = []     # collections.deque() seems slightly slower
        self.vars = novalue
        self.pid = None      # assigned lazily

    def __repr__(self):
        return "Context(" + str(self.nametag) + ", " + str(self.pc) + ")"

    def __hash__(self):
        h = (self.nametag, self.pc, self.end,
                    self.atomic, self.vars, self.pid).__hash__()
        for v in self.stack:
            h ^= v.__hash__()
        return h

    def __eq__(self, other):
        if not isinstance(other, Context):
            return False
        if self.nametag != other.nametag:
            return False
        if self.pc != other.pc:
            return False
        if self.atomic != other.atomic:
            return False
        # !!!
        if self.pid != other.pid:
            return False
        assert self.end == other.end
        return self.stack == other.stack and self.vars == other.vars

    def copy(self):
        c = Context(self.nametag, self.pc, self.end)
        c.atomic = self.atomic
        c.stack = self.stack.copy()
        c.vars = self.vars
        c.pid = self.pid
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
        return DictValue(d)

    def set(self, indexes, val):
        self.vars = self.update(self.vars, indexes, val)

    def push(self, val):
        assert val != None
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

class State:
    def __init__(self, code, labels):
        self.code = code
        self.labels = labels
        self.vars = novalue
        self.ctxbag = {
            Context(DictValue({"name": "__main__", "tag": novalue}), 0, len(code)) : 1
        }
        self.failure = False

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
        assert self.code == other.code and self.labels == other.labels
        if self.vars != other.vars:
            return False
        if self.ctxbag != other.ctxbag:
            return False
        if self.failure != other.failure:
            return False
        return True

    def copy(self):
        s = State(self.code, self.labels)
        s.vars = self.vars      # no need to copy as store operations do it
        s.ctxbag = self.ctxbag.copy()
        s.failure = self.failure
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
        return DictValue(d)

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
        self.parent = parent    # next hop on way to initial state
        self.len = len          # length of path to initial state
        self.ctx = ctx          # the context that made the hop from the parent state
        self.choice = choice    # maybe None if no choice was made
        self.steps = steps      # list of microsteps
        self.edges = {}         # forward edges (ctx -> <nextState, nextContext, steps>)
        self.sources = set()    # backward edges
        self.expanded = False   # lazy deletion

def strsteps(steps):
    if steps == None:
        return "[]"
    result = ""
    i = 0
    while i < len(steps):
        if result != "":
            result += ","
        result += str(steps[i])
        j = i + 1
        while j < len(steps) and steps[j] == steps[j - 1] + 1:
            j += 1
        if j > i + 1:
            result += "-" + str(steps[j - 1])
        i = j
    return "[" + result + "]"

def get_path(visited, state):
    if state == None:
        return []
    node = visited[state]
    return get_path(visited, node.parent) + [(node, state.vars)]

def print_shortest(visited, bad):
    best_state = None
    best_len = 0
    for s in bad:
        node = visited[s]
        if best_state == None or node.len < best_len:
            best_state = s
            best_len = node.len
    path = get_path(visited, best_state)[1:]
    last = None
    for (node, vars) in path:
        if last == None:
            last = (node.ctx.nametag, node.ctx.pc, node.steps, vars)
        elif node.ctx.nametag == last[0] and node.steps[0] == last[1]:
            last = (node.ctx.nametag, node.ctx.pc, last[2] + node.steps, vars)
        else:
            print(last[0], strsteps(last[2]), last[1], last[3])
            last = (node.ctx.nametag, node.ctx.pc, node.steps, vars)
    if last != None:
        print(last[0], strsteps(last[2]), last[1], last[3])

class Scope:
    def __init__(self, parent):
        self.parent = parent
        self.names = {}
        self.locations = {}
        self.labels = {}

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

    def location(self, pc, file, line, labels):
        if self.parent == None:
            self.locations[pc] = (file, line)
            for (label, file, line, column) in labels:
                self.labels[label] = pc
        else:
            self.parent.location(pc, file, line, labels)

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
        elif isinstance(op, JumpCondOp):
            code[i] = JumpCondOp(op.cond, optjump(code, op.pc))

# These operations cause global state changes
globops = [
    AtomicIncOp, LoadOp, SpawnOp, StoreOp
]

# Have context ctx make one (macro) step in the given state
def onestep(state, ctx, choice, visited, todo, node, infloop):
    # Keep track of whether this is the same context as the parent context
    samectx = ctx == node.ctx

    # Copy the state
    sc = state.copy()   # sc is "state copy"

    # Make a copy of the context before modifying it (cc is "context copy")
    cc = ctx.copy()

    if choice == None:
        steps = []
    else:
        steps = [cc.pc]
        cc.stack[-1] = choice
        cc.pc += 1

    localStates = { cc.copy() }
    foundInfLoop = False
    while cc.pc != cc.end:
        # execute one microstep
        steps.append(cc.pc)

        try:
            sc.code[cc.pc].eval(sc, cc)
        except Exception as e:
            traceback.print_exc()
            sc.failure = True

        # TODO.  Checking for end twice in this loop seems wrong
        if sc.failure or cc.pc == cc.end:
            break

        # if we're about to do a state change, let other processes
        # go first assuming there are other processes and we're not
        # in "atomic" mode
        if isinstance(sc.code[cc.pc], ChooseOp):
            v = cc.stack[-1]
            assert isinstance(v, SetValue), v
            if len(v.s) != 1:
                break
        if cc.atomic == 0 and type(sc.code[cc.pc]) in globops and len(sc.ctxbag) > 0:
            break

        # Detect infinite loops
        if cc in localStates:
            foundInfLoop = True
            break
        localStates.add(cc.copy())

    # Remove original context from bag
    sc.remove(ctx)

    # Put the resulting context into the bag unless it's done
    if cc.pc != cc.end:
        sc.add(cc)

    length = node.len if samectx else (node.len + 1)
    next = visited.get(sc)
    if next == None:
        next = Node(state, cc, choice, steps, length)
        visited[sc] = next
        if samectx:
            todo.insert(0, sc)
        else:
            todo.append(sc)
    elif next.len > length:
        assert length == node.len and next.len == node.len + 1 and not next.expanded, (node.len, length, next.len, next.expanded)
        # assert not next.expanded, (node.len, length, next.len, next.expanded)
        next.len = length
        next.parent = state
        next.ctx = cc
        next.steps = steps
        next.choice = choice
        todo.insert(0, sc)
    node.edges[ctx] = (sc, cc, steps)
    next.sources.add(state)

    if foundInfLoop:
        infloop.add(sc)

def compile(f, filename):
    scope = Scope(None)
    code = []
    load(f, filename, scope, code)
    optimize(code)

    lastloc = None
    for pc in range(len(code)):
        if scope.locations.get(pc) != None:
            (file, line) = scope.locations[pc]
            if (file, line) != lastloc:
                lines = files.get(file)
                if lines != None and line <= len(lines):
                    print(file, ":", line, lines[line - 1][0:-1])
                else:
                    print(file, ":", line)
            lastloc = (file, line)
        print("  ", pc, code[pc])
    return (code, scope.labels)

# See if some process other than ctx can reach cs
def canReach(visited, s, ctx, cs, ncs, checked):
    if s in checked:        # check for loop
        return False
    checked.add(s)
    next = visited[s].edges.get(ctx)
    if next == None:        # check for process termination
        return False
    (nextState, nextContext, steps) = next
    if pc in steps:
        return True
    return canReach(visited, nextState, nextContext, pc, checked)

def run(code, labels):
    # Initial state
    state = State(code, labels)

    # For traversing Kripke graph
    visited = { state: Node(None, None, None, None, 0) }
    todo = collections.deque([state])
    bad = set()
    infloop = set()

    cnt = 0
    faultyState = False
    while todo:
        state = todo.popleft()
        if state.failure:
            bad.add(state)
            faultyState = True
            break           # TODO: should this be a continue?
        node = visited[state]
        cnt += 1
        # if cnt % 10000 == 0 :
        #    print(state)
        print(" ", cnt, "#states =", len(visited.keys()), "diameter =", node.len, "queue =", len(todo), end="     \r")
        if node.expanded:
            continue
        node.expanded = True

        for (ctx, _) in state.ctxbag.items():
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
    elif not faultyState:
        # See if all processes "can" terminate.  First looks for states where
        # there are no processes.
        term = set()
        for s in visited.keys():
            if len(s.ctxbag) == 0:
                term.add(s)
        # Now find all the states that can reach terminating states.
        nextgood = term
        while nextgood != set():
            newgood = set()
            for s in nextgood:
                for s2 in visited[s].sources.difference(term):
                    newgood.add(s2)
            term = term.union(newgood)
            nextgood = newgood
        bad = set(visited.keys()).difference(term)
        if len(bad) > 0:
            print("==== Non-terminating States ====", len(bad))
            print_shortest(visited, bad)

    return visited

def main():
    (code, labels) = compile(sys.stdin, "<stdin>")
    run(code, labels)

if __name__ == "__main__":
    main()
