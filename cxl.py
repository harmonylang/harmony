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
        "getpid",
        "if",
        "import",
        "in",
        "keys",
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
    return s in [ "^", "-", "atLabel", "cardinality", "getpid", "not", "keys" ]

def isbinaryop(s):
    return s in [
        "==", "!=", "..", "\\", "in", "and", "or",
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
            state.failure = True
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
            (lexeme, file, line, column) = self.arg
            context.vars = RecordValue({ lexeme: arg })
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
    def __repr__(self):
        return "Set"

    def eval(self, state, context):
        nitems = context.pop()
        s = set()
        for i in range(nitems):
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

    def atLabel(self, state, label):
        pc = state.labels[label]
        d = {}
        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc == pc:
                c = d.get(ctx.tag)
                d[ctx.tag] = 1 if c == None else (c + 1)
        return RecordValue(d)

    def eval(self, state, context):
        (op, file, line, column) = self.op
        if self.n == 1:
            e = context.pop()
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
            elif op == "getpid":
                assert isinstance(e, NoValue), e
                if context.pid == None:
                    state.pidgen += 1
                    context.pid = state.pidgen
                context.push(context.pid)
            elif op == "keys":
                assert isinstance(e, RecordValue), e
                context.push(SetValue(set(e.d.keys())))
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
            elif t == "method":
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
        code.append(ConstantOp((len(self.collection), None, None, None)))
        code.append(SetOp())

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
        code.append(NaryOp(("cardinality", file, line, column), 1))
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
        code[tst] = JumpFalseOp(len(code))
        code.append(LoadVarOp(N))
        code.append(SetOp())

class RecordComprehensionAST(AST):
    def __init__(self, value, var, expr):
        self.value = value
        self.var = var
        self.expr = expr

    def __repr__(self):
        return "RecordComprehension(" + str(self.var) + ")"

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
        code.append(NaryOp(("cardinality", file, line, column), 1))
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
    def __init__(self, closers):
        self.closers = closers

    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        if isunaryop(lexeme):
            op = t[0]
            (ast, t) = BasicExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme in self.closers, t[0]
            return (NaryAST(op, [ast]), t)
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

class RecordComprehensionRule(Rule):
    def __init__(self, value):
        self.value = value

    def parse(self, t):
        name = t[0]
        (lexeme, file, line, column) = name
        assert isname(lexeme), name
        (lexeme, file, line, column) = t[1]
        assert lexeme == "in", t[1]
        (expr, t) = NaryRule({"}"}).parse(t[2:])
        return (RecordComprehensionAST(self.value, name, expr), t[1:])

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

class RecordRule(Rule):
    def parse(self, t):
        (lexeme, file, line, column) = t[0]
        assert lexeme == "dict{", t[0]
        d = {}
        while lexeme != "}":
            (key, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            if lexeme == "for":
                assert d == {}, d
                return RecordComprehensionRule(key).parse(t[1:])
            assert lexeme == ":", t[0]
            (value, t) = NaryRule({",", "}"}).parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme in { ",", "}" }, t[0]
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
            return RecordRule().parse(t)
        if lexeme == "(" or lexeme == "[":
            closer = ")" if lexeme == "(" else "]"
            (lexeme, file, line, column) = t[1]
            if lexeme == closer:
                return (ConstantAST(
                    (NoValue(), file, line, column)), t[2:])
            (ast, t) = NaryRule({closer}).parse(t[1:])
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
        code.append(NaryOp(("cardinality", file, line, column), 1))
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
        code[tst] = JumpFalseOp(len(code))

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
        self.expr.compile(scope, code)
        code.append(AssertOp(self.token))
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
        code[pc+1] = FrameOp(self.name, self.arg, len(code) - 1)
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
            assert isinstance(ast, ConstantAST), ast
            return (ConstAST(const, ast.const), self.skip(token, t))
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
            method = t[1]
            (lexeme, file, line, column) = method
            assert isname(lexeme), method
            (expr, t) = ExpressionRule().parse(t[2:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ",", t[0]
            (tag, t) = ExpressionRule().parse(t[1:])
            (lexeme, file, line, column) = t[0]
            assert lexeme == ";", t[0]
            return (SpawnAST(tag, method, expr), self.skip(token, t))
        if lexeme == "pass":
            return (PassAST(), self.skip(token, t[1:]))
        if lexeme == "import":
            (lexeme, file, line, column) = t[1]
            assert isname(lexeme), t[1]
            return (ImportAST(t[1]), self.skip(token, t[2:]))
        if lexeme == "assert":
            (cond, t) = NaryRule({","}).parse(t[1:])
            (expr, t) = NaryRule({";"}).parse(t[1:])
            return (AssertAST(token, cond, expr), self.skip(token, t))
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
        self.pid = None      # assigned lazily

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
        # !!!
        if self.pid != other.pid:
            return False
        assert self.end == other.end
        return self.stack == other.stack and self.vars == other.vars

    def copy(self):
        c = Context(self.name, self.tag, self.pc, self.end)
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
        return RecordValue(d)

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
        self.vars = RecordValue({})
        self.ctxbag = { Context("__main__", 0, 0, len(code)) : 1 }
        self.failure = False
        self.pidgen = 0     # to generate pids

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
        if self.pidgen != other.pidgen:
            return False
        return True

    def copy(self):
        s = State(self.code, self.labels)
        s.vars = self.vars      # no need to copy as store operations do it
        s.ctxbag = self.ctxbag.copy()
        s.failure = self.failure
        s.pidgen = self.pidgen
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
        self.parent = parent    # next hop on way to initial state
        self.len = len          # length of path to initial state
        self.ctx = ctx          # the context that made the hop from the parent state
        self.choice = choice    # maybe None if no choice was made
        self.steps = steps      # list of microsteps
        self.edges = {}         # forward edges (ctx -> state)
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
            last = (node.ctx.name, node.ctx.tag, node.ctx.pc, node.steps, vars)
        elif node.ctx.name == last[0] and node.ctx.tag == last[1] and \
                                            node.steps[0] == last[2]:
            last = (node.ctx.name, node.ctx.tag, node.ctx.pc, last[3] + node.steps, vars)
        else:
            print(last[0], last[1], strsteps(last[3]), last[2], last[4])
            last = (node.ctx.name, node.ctx.tag, node.ctx.pc, node.steps, vars)
    if last != None:
        print(last[0], last[1], strsteps(last[3]), last[2], last[4])

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
        elif isinstance(op, JumpFalseOp):
            code[i] = JumpFalseOp(optjump(code, op.pc))

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
    while True:
        # execute one microstep
        steps.append(cc.pc)

        try:
            sc.code[cc.pc].eval(sc, cc)
        except Exception as e:
            traceback.print_exc()
            sc.failure = True

        if sc.failure:
            break

        # if we reached the end, remove the context
        if cc.pc == cc.end:
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
    node.edges[ctx] = (sc, steps)
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

def run(code, labels, invariant, pcs):
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
        if cnt % 10000 == 0 :
            print(state)
        print(" ", cnt, "#states =", len(visited.keys()), "diameter =", node.len, "queue =", len(todo), end="     \r")
        if node.expanded:
            continue
        node.expanded = True


        if not invariant(state):
            bad.add(state)

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

    if not faultyState:
        # See if there are livelocked states (states from which some process
        # cannot reach the reader or writer critical section)
        bad = set()
        for (p, cs) in pcs:
            # First collect all the states in which the process is in the
            # critical region
            good = set()
            for (s, node) in visited.items():
                for (ctx, edge) in node.edges.items():
                    (next, steps) = edge
                    if (ctx.name, ctx.tag) == p and (cs in steps):
                        good.add(next)
                        good.add(s)     # might as well add this now

            # All the states reachable from good are good too
            nextgood = good
            while nextgood != set():
                newgood = set()
                for s in nextgood:
                    for s2 in visited[s].sources.difference(good):
                        newgood.add(s2)
                good = good.union(newgood)
                nextgood = newgood
            livelocked = set(visited.keys()).difference(good)
            bad = bad.union(livelocked)
        if len(bad) > 0:
            print("==== Livelock ====", len(bad))
            print_shortest(visited, bad)

    return visited
