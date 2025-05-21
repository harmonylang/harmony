import math
from typing import Any, Dict, Optional, Set, Union
from harmony_model_checker.harmony.state import State
from harmony_model_checker.harmony.value import *
from harmony_model_checker.harmony.bag_util import *

def _prefix_name(prefix, name):
    if prefix is None:
        return name
    else:
        return prefix + '$' + name

class Op:
    def define(self):   # set of local variables updated by this op
        return set()

    def use(self):      # set of local variables used by this op
        return set()

    def jdump(self):
        return '{ "op": "XXX %s" }'%str(self)

    def tladump(self):
        return 'Skip(self, "%s")'%self

    def explain(self):
        return "no explanation yet"

    def eval(self, state: State, context: ContextValue):
        ...

    def sametype(x: Any, y: Any) -> bool:
        return type(x) == type(y)

    def convert(self, x) -> str:
        if isinstance(x, tuple):
            return x[0]
        else:
            assert isinstance(x, list)
            result = ""
            for v in x:
                if result != "":
                    result += ", "
                result += self.convert(v)
            return "(" + result + ")"

    def tlaconvert(self, x):
        if isinstance(x, tuple):
            return 'VName("%s")'%x[0]
        else:
            assert isinstance(x, list)
            result = 'VList(<< '
            result += ",".join([self.tlaconvert(v) for v in x])
            return result + " >>)"

    # Return the set of local variables in x
    # TODO.  Use reduce()
    def lvars(self, x) -> Set[str]:
        if isinstance(x, tuple):
            return { x[0] }
        else:
            assert isinstance(x, list)
            result = set()
            for v in x:
                result |= self.lvars(v)
            return result

    def store(self, context: ContextValue, var: Union[tuple, list], val: DictValue):
        if isinstance(var, tuple):
            (lexeme, file, line, column) = var
            context.set([lexeme], val)
        else:
            assert isinstance(var, list)
            if not isinstance(val, DictValue):
                context.failure = "Error: pc = %d: tried to assign %s to %s"%(
                    context.pc, val, self.convert(var))
            elif len(var) != len(val.d):
                context.failure = "Error: pc = %d: cannot assign %s to %s"%(
                    context.pc, val, self.convert(var))
            else:
                for i in range(len(var)):
                    self.store(context, var[i], val.d[i])

    def load(self, context: ContextValue, var: Union[tuple, list]):
        if isinstance(var, tuple):
            (lexeme, file, line, column) = var
            return context.get(lexeme)
        else:
            assert isinstance(var, list)
            d = { i:self.load(context, var[i]) for i in range(len(var)) }
            return DictValue(d)

    def substitute(self, map):
        pass

class SetIntLevelOp(Op):
    def __repr__(self):
        return "SetIntLevel"

    def jdump(self):
        return '{ "op": "SetIntLevel" }'

    def tladump(self):
        return 'OpSetIntLevel(self)'

    def explain(self):
        return "pops new boolean interrupt level and pushes old one"

    def eval(self, state, context):
        before = context.interruptLevel
        v = context.pop()
        assert isinstance(v, bool), v
        context.interruptLevel = v
        context.push(before)
        context.pc += 1

# Splits a non-empty set or dict in its minimum element and its remainder
class CutOp(Op):
    def __init__(self, value, key):
        self.value = value
        self.key = key

    def __repr__(self):
        if self.key is None:
            return "Cut(" + self.convert(self.value) + ")"
        else:
            return "Cut(" + self.convert(self.key) + ", " + self.convert(self.value) + ")"

    def define(self):
        if self.key is None:
            return self.lvars(self.value)
        else:
            return self.lvars(self.value) | self.lvars(self.key)

    def jdump(self):
        if self.key is None:
            return '{ "op": "Cut", "value": "%s" }'%(self.convert(self.value))
        else:
            return '{ "op": "Cut", "key": "%s", "value": "%s" }'%(self.convert(self.key), self.convert(self.value))

    def tladump(self):
        if self.key is None:
            return 'OpCut(self, %s)'%(self.tlaconvert(self.value))
        else:
            return 'OpCut2(self, %s, %s)'%(
                        self.tlaconvert(self.value), self.tlaconvert(self.key))

    def explain(self):
        suffix = "; push False or True depending on success"
        if self.key is None:
            return "get next element and assign to %s"%(self.convert(self.value)) + suffix
        else:
            return "get next element and assign to %s:%s"%(self.convert(self.key), self.convert(self.value)) + suffix

    def eval(self, state, context):
        assert False
        key = self.load(context, self.s)
        if isinstance(key, DictValue):
            if key.d == {}:
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: expected non-empty dict value"
            else:
                select = min(key.d.keys(), key=keyValue)
                self.store(context, self.key, key.d[select])
                copy = key.d.copy()
                del copy[select]
                self.store(context, self.s, DictValue(copy))
                context.pc += 1
        else:
            if not isinstance(key, SetValue):
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: expected set value, got " + str(key)
            elif key.s == set():
                context.failure = "pc = " + str(context.pc) + \
                    ": Error: expected non-empty set value"
            else:
                lst = sorted(key.s, key=keyValue)
                self.store(context, self.key, lst[0])
                self.store(context, self.s, SetValue(set(lst[1:])))
                context.pc += 1

# Splits a tuple into its elements
class SplitOp(Op):
    def __init__(self, n):
        self.n = n

    def __repr__(self):
        return "Split %d"%self.n

    def jdump(self):
        return '{ "op": "Split", "count": "%d" }'%self.n

    def tladump(self):
        return 'OpSplit(self, %d)'%self.n

    def explain(self):
        return "splits a tuple value into its elements"

    def eval(self, state, context):
        v = context.pop()
        assert isinstance(v, DictValue), v
        assert len(v.d) == self.n, (self.n, len(v.d))
        for i in range(len(v.d)):
            context.push(v.d[i])
        context.pc += 1

# Move an item in the stack to the top
class MoveOp(Op):
    def __init__(self, offset):
        self.offset = offset

    def __repr__(self):
        return "Move %d"%self.offset

    def jdump(self):
        return '{ "op": "Move", "offset": "%d" }'%self.offset

    def tladump(self):
        return 'OpMove(self, %d)'%self.offset

    def explain(self):
        return "move stack element to top"

    def eval(self, state, context):
        v = context.stack.pop(len(context.stack) - self.offset)
        context.push(v)
        context.pc += 1

class DupOp(Op):
    def __repr__(self):
        return "Dup"

    def jdump(self):
        return '{ "op": "Dup" }'

    def tladump(self):
        return 'OpDup(self)'

    def explain(self):
        return "push a copy of the top value on the stack"

    def eval(self, state, context):
        v = context.pop()
        context.push(v)
        context.push(v)
        context.pc += 1

class GoOp(Op):
    def __repr__(self):
        return "Go"

    def jdump(self):
        return '{ "op": "Go" }'

    def tladump(self):
        return 'OpGo(self)'

    def explain(self):
        return "pops a context and a value, restores the corresponding thread, and pushes the value on its stack"

    def eval(self, state, context):
        ctx = context.pop()
        if not isinstance(ctx, ContextValue):
            context.failure = "pc = " + str(context.pc) + \
                ": Error: expected context value, got " + str(ctx)
        else:
            if ctx in state.stopbag:
                cnt = state.stopbag[ctx]
                assert cnt > 0
                if cnt == 1:
                    del state.stopbag[ctx]
                else:
                    state.stopbag[ctx] = cnt - 1
            result = context.pop();
            copy = ctx.copy()
            copy.push(result)
            copy.stopped = False
            bag_add(state.ctxbag, copy)
            context.pc += 1

class ApplyOp(Op):
    def __init__(self, method):
        self.method = method

    def __repr__(self):
        (lexeme, file, line, column) = self.method
        return "Apply %s"%strValue(lexeme)

    def jdump(self):
        (lexeme, file, line, column) = self.method
        return '{ "op": "Apply", "value": %s }'%jsonValue(lexeme)

    def tladump(self):
        (lexeme, file, line, column) = self.method
        return 'OpApply(self, %d)'%self.method[0].pc

    def explain(self):
        return "call method " + strValue(self.method[0])

    def eval(self, state, context):
        assert False

    def substitute(self, map):
        (lexeme, file, line, column) = self.method
        if isinstance(lexeme, Value):
            self.method = (lexeme.substitute(map), file, line, column)


class LoadVarOp(Op):
    def __init__(self, v, lvar=None, reason=None):
        assert v is not None        # TODO.  LoadVarOp(None) is obsolete
        self.v = v
        self.lvar = lvar        # name of local var if v is None
        self.reason = reason

    def __repr__(self):
        return "LoadVar " + self.convert(self.v)

    def define(self):
        return set()

    def use(self):
        return self.lvars(self.v)

    def jdump(self):
        return '{ "op": "LoadVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        return 'OpLoadVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        if self.reason is None:
            prefix = ""
        else:
            prefix = self.reason + ": "
        return prefix + "push the value of " + self.convert(self.v)

    def eval(self, state, context):
        context.push(self.load(context, self.v))
        context.pc += 1

class PushOp(Op):
    def __init__(self, constant: Tuple[Any, Optional[str], Optional[int], Optional[int]], reason: Optional[str] =None):
        self.constant = constant
        self.reason = reason

    def __repr__(self):
        (lexeme, file, line, column) = self.constant
        return "Push %s"%strValue(lexeme)

    def jdump(self):
        (lexeme, file, line, column) = self.constant
        return '{ "op": "Push", "value": %s }'%jsonValue(lexeme)

    def tladump(self):
        (lexeme, file, line, column) = self.constant
        v = tlaValue(lexeme)
        return 'OpPush(self, %s)'%v

    def explain(self):
        prefix = "" if self.reason is None else (self.reason + ": ")
        return prefix + "push constant " + strValue(self.constant[0])

    def eval(self, state, context):
        (lexeme, file, line, column) = self.constant
        context.push(lexeme)
        context.pc += 1

    def substitute(self, map):
        (lexeme, file, line, column) = self.constant
        if isinstance(lexeme, Value):
            self.constant = (lexeme.substitute(map), file, line, column)

class LoadOp(Op):
    def __init__(self, name, token, prefix):
        self.name = name
        self.token = token
        self.prefix = prefix

    def __repr__(self):
        if self.name is None:
            return "Load"
        else:
            (lexeme, file, line, column) = self.name
            return "Load " + _prefix_name(self.prefix, lexeme)

    def jdump(self):
        if self.name is None:
            return '{ "op": "Load" }'
        else:
            (lexeme, file, line, column) = self.name
            return '{ "op": "Load", "value": [{ "type": "atom", "value": "%s"}] }'%_prefix_name(self.prefix, lexeme)

    def tladump(self):
        if self.name is None:
            return "OpLoadInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            return 'OpLoad(self, HStr("%s"))'%_prefix_name(self.prefix, lexeme)

    def explain(self):
        if self.name is None:
            return "pop an address and push the value at the address"
        else:
            return "push value of shared variable " + self.name[0]

    def eval(self, state, context):
        if self.name is None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.token) + " -> " + str(av)
                return
            context.push(state.iget(av.indexes()))
        else:
            (lexeme, file, line, column) = self.name
            # TODO
            if False and lexeme not in state.vars.d:
                context.failure = "Error: no variable " + str(self.token)
                return
            context.push(state.iget([_prefix_name(self.prefix, lexeme)]))
        context.pc += 1

class StoreOp(Op):
    def __init__(self, name, token, prefix):
        self.name = name
        self.token = token  # for error reporting
        self.prefix = prefix
        assert not isinstance(prefix, list)

    def __repr__(self):
        if self.name is None:
            return "Store"
        else:
            (lexeme, file, line, column) = self.name
            return "Store " + _prefix_name(self.prefix, lexeme)

    def jdump(self):
        if self.name is None:
            return '{ "op": "Store" }'
        else:
            (lexeme, file, line, column) = self.name
            return '{ "op": "Store", "value": [{ "type": "atom", "value": "%s"}] }'%_prefix_name(self.prefix, lexeme)

    def tladump(self):
        if self.name is None:
            return "OpStoreInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            return 'OpStore(self, <<HStr("%s")>>)'%_prefix_name(self.prefix, lexeme)

    def explain(self):
        if self.name is None:
            return "pop a value and an address and store the value at the address"
        else:
            return "pop a value and store it in shared variable " + self.name[0]

    def eval(self, state, context):
        if context.readonly > 0:
            context.failure = "Error: no update allowed in assert " + str(self.token)
            return
        v = context.pop()
        if self.name is None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.token) + " -> " + str(av)
                return
            lv = av.indexes()
            if len(lv) == 0:
                context.failure = "Error: bad address " + str(self.token)
                return
            name = lv[0]
        else:
            (lexeme, file, line, column) = self.name
            lv = [_prefix_name(self.prefix, lexeme)]
            name = lexeme

        # TODO
        if False and not state.initializing and (name not in state.vars.d):
            context.failure = "Error: using an uninitialized shared variable " \
                    + name + ": " + str(self.token)
        else:
            try:
                state.set(lv, v)
                context.pc += 1
            except AttributeError:
                context.failure = "Error: " + name + " is not a dictionary " + str(self.token)

class DelOp(Op):
    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix

    def __repr__(self):
        if self.name is not None:
            (lexeme, file, line, column) = self.name
            return "Del " + _prefix_name(self.prefix, lexeme)
        else:
            return "Del"

    def jdump(self):
        if self.name is None:
            return '{ "op": "Del" }'
        else:
            (lexeme, file, line, column) = self.name
            return '{ "op": "Del", "value": [{ "type": "atom", "value": "%s"}] }'%_prefix_name(self.prefix, lexeme)

    def tladump(self):
        if self.name is None:
            return "OpDelInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            return 'OpDel(self, <<"%s">>)'%_prefix_name(self.prefix, lexeme)

    def explain(self):
        if self.name is None:
            return "pop an address and delete the shared variable at the address"
        else:
            return "delete the shared variable " + self.name[0]

    def eval(self, state, context):
        if self.name is None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.name) + " -> " + str(av)
                return
            lv = av.indexes()
            name = lv[0]
        else:
            (lexeme, file, line, column) = self.name
            lv = [lexeme]
            name = lexeme

        if not state.initializing and (name not in state.vars.d):
            context.failure = "Error: deleting an uninitialized shared variable " \
                    + name + ": " + str(self.name)
        else:
            state.delete(lv)
            context.pc += 1

class SaveOp(Op):
    def __repr__(self):
        return "Save"

    def jdump(self):
        return '{ "op": "Save" }'

    def tladump(self):
        return "OpSave(self)"

    def explain(self):
        return "pop a value and save context"

    def eval(self, state, context):
        assert False

class StopOp(Op):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        if self.name is not None:
            (lexeme, file, line, column) = self.name
            return "Stop " + lexeme
        else:
            return "Stop"

    def jdump(self):
        if self.name is not None:
            (lexeme, file, line, column) = self.name
            return '{ "op": "Stop", "value": %s }'%lexeme
        else:
            return '{ "op": "Stop" }'

    def tladump(self):
        if self.name is None:
            return "OpStopInd(self)"
        else:
            (lexeme, file, line, column) = self.name
            return "OpStop(self, %s)"%lexeme

    def explain(self):
        if self.name is None:
            return "pop an address and store context at that address"
        else:
            return "store context at " + self.name[0]

    def eval(self, state, context):
        if self.name is None:
            av = context.pop()
            if not isinstance(av, AddressValue):
                context.failure = "Error: not an address " + \
                                    str(self.name) + " -> " + str(av)
                return
            lv = av.indexes()
            name = lv[0]
        else:
            (lexeme, file, line, column) = self.name
            lv = [lexeme]
            name = lexeme

        if not state.initializing and (name not in state.vars.d):
            context.failure = "Error: using an uninitialized shared variable " \
                    + name + ": " + str(self.name)
        else:
            # Update the context before saving it
            context.stopped = True
            context.pc += 1
            assert isinstance(state.code[context.pc], ContinueOp)

            # Save the context
            state.stop(lv, context)

class BuiltinOp(Op):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "Builtin(%s)"%self.value

    def jdump(self):
        return '{ "op": "Builtin", "value": "%s" }'%self.value

    def tladump(self):
        pass

    def explain(self):
        return "top of stack is a built-in operation called %s"%self.value

    def eval(self, state, context):
        context.pop()

class SequentialOp(Op):
    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return "Sequential"

    def jdump(self):
        lexeme, file, line, column = self.var
        return '{ "op": "Sequential", "var": "%s" }' % lexeme

    def tladump(self):
        return 'OpSequential(self)'

    def explain(self):
        lexeme, file, line, column = self.var
        return "sequential consistency for %s" % lexeme

    def eval(self, state, context):
        # TODO
        context.pop()

class ContinueOp(Op):
    def __repr__(self):
        return "Continue"

    def explain(self):
        return "a no-op, must follow a Stop or Save operation"

    def jdump(self):
        return '{ "op": "Continue" }'

    def tladump(self):
        return 'OpContinue(self)'

    def eval(self, state, context):
        context.pc += 1

class StoreVarOp(Op):
    def __init__(self, v, lvar=None, reason=None):
        self.v = v
        self.lvar = lvar        # name of local var if v is None
        self.reason = reason

    def __repr__(self):
        if self.v is None:
            return "StoreVar [%s]"%self.lvar
        else:
            return "StoreVar " + self.convert(self.v)

    # In case of StoreVar(x[?]), x does not get defined, only used
    def define(self):
        if self.v is None:
            return set()
        return self.lvars(self.v)

    # if v is None, only part of self.lvar is updated--the rest is used
    def use(self):
        if self.v is None:
            return { self.lvar }
        return set()

    def jdump(self):
        if self.v is None:
            return '{ "op": "StoreVar" }'
        else:
            return '{ "op": "StoreVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        if self.v is None:
            return 'OpStoreVarInd(self)'
        else:
            return 'OpStoreVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        if self.reason is None:
            prefix = ""
        else:
            prefix = self.reason + ": "
        if self.v is None:
            return prefix + "pop a value and the address of a method variable and store the value at that address"
        else:
            return prefix + "pop a value and store in " + self.convert(self.v)

    # TODO.  Check error message.  Doesn't seem right
    def eval(self, state, context):
        if self.v is None:
            value = context.pop()
            av = context.pop()
            assert isinstance(av, AddressValue)
            try:
                context.set(av.indexes(), value)
                context.pc += 1
            except AttributeError:
                context.failure = "Error: " + str(av.indexes()) + " not a dictionary"
        else:
            try:
                self.store(context, self.v, context.pop())
                context.pc += 1
            except AttributeError:
                context.failure = "Error: " + str(self.v) + " -- not a dictionary"

class DelVarOp(Op):
    def __init__(self, v, lvar=None):
        self.v = v
        self.lvar = lvar

    def __repr__(self):
        if self.v is None:
            return "DelVar [%s]"%self.lvar
        else:
            (lexeme, file, line, column) = self.v
            return "DelVar " + str(lexeme)

    # if v is None, self.lvar is used but not defined
    def define(self):
        if self.v is None:
            return set()
        return self.lvars(self.v)

    # if v is None, only part of self.lvar is deleted--the rest is used
    def use(self):
        if self.v is None:
            return { self.lvar }
        return set()

    def jdump(self):
        if self.v is None:
            return '{ "op": "DelVar" }'
        else:
            return '{ "op": "DelVar", "value": "%s" }'%self.convert(self.v)

    def tladump(self):
        if self.v is None:
            return 'OpDelVarInd(self)'
        else:
            return 'OpDelVar(self, %s)'%self.tlaconvert(self.v)

    def explain(self):
        if self.v is None:
            return "pop an address of a method variable and delete that variable"
        else:
            return "delete method variable " + self.v[0]

    def eval(self, state, context):
        if self.v is None:
            av = context.pop()
            assert isinstance(av, AddressValue)
            context.delete(av.indexes())
        else:
            (lexeme, file, line, column) = self.v
            context.delete([lexeme])
        context.pc += 1

class ChooseOp(Op):
    def __repr__(self):
        return "Choose"

    def jdump(self):
        return '{ "op": "Choose" }'

    def tladump(self):
        return 'OpChoose(self)'

    def explain(self):
        return "pop a set value and push one of its elements"

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
        return "Assert2" if self.exprthere else "Assert"

    def jdump(self):
        if self.exprthere:
            return '{ "op": "Assert2" }'
        else:
            return '{ "op": "Assert" }'

    def tladump(self):
        (lexeme, file, line, column) = self.token
        msg = '"Harmony Assertion (file=%s, line=%d) failed"'%(file, line)
        if self.exprthere:
            return 'OpAssert2(self, %s)'%msg
        else:
            return 'OpAssert(self, %s)'%msg

    def explain(self):
        if self.exprthere:
            return "pop a value and a condition and raise exception if condition is false"
        else:
            return "pop a condition and raise exception if condition is false"

    def eval(self, state, context):
        if self.exprthere:
            expr = context.pop()
        cond = context.pop()
        if not isinstance(cond, bool):
            context.failure = "Error: argument to " + str(self.token) + \
                        " must be a boolean: " + strValue(cond)
            return
        if not cond:
            (lexeme, file, line, column) = self.token
            context.failure = "Harmony Assertion (file=%s, line=%d) failed"%(file, line)
            if self.exprthere:
                context.failure += ": " + strValue(expr)
            return
        context.pc += 1

class PrintOp(Op):
    def __init__(self, token, attrsthere):
        self.token = token
        self.attrsthere = attrsthere

    def __repr__(self):
        return "Print"

    def jdump(self):
        return '{ "op": "Print", "attrs": %d }'%(1 if self.attrsthere else 0)

    def tladump(self):
        return 'OpPrint(self)'

    def explain(self):
        return "pop a value and add to print history"

    def eval(self, state, context):
        cond = context.pop()
        context.pc += 1
        assert False

class PossiblyOp(Op):
    def __init__(self, token, index):
        self.token = token
        self.index = index

    def __repr__(self):
        return "Possibly %d"%self.index

    def jdump(self):
        return '{ "op": "Possibly", "index": "%d" }'%self.index

    def explain(self):
        return "pop a condition and check"

class PopOp(Op):
    def __init__(self):
        pass

    def __repr__(self):
        return "Pop"

    def jdump(self):
        return '{ "op": "Pop" }'

    def tladump(self):
        return 'OpPop(self)'

    def explain(self):
        return "discard the top value on the stack"

    def eval(self, state, context):
        context.pop()
        context.pc += 1

class FrameOp(Op):
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        (lexeme, file, line, column) = self.name
        args = self.convert(self.args)
        if args[0] == "(":
            return "Frame " + str(lexeme) + args
        return "Frame " + str(lexeme) + "(" + args + ")"

    def define(self):
        return self.lvars(self.args) | { "result" }

    def jdump(self):
        (lexeme, file, line, column) = self.name
        return '{ "op": "Frame", "name": "%s", "args": "%s" }'%(lexeme, self.convert(self.args))

    def tladump(self):
        (lexeme, file, line, column) = self.name
        return 'OpFrame(self, "%s", %s)'%(lexeme, self.tlaconvert(self.args))

    def explain(self):
        return "start of method " + str(self.name[0])

    def eval(self, state, context):
        arg = context.pop()
        context.push(arg)               # restore for easier debugging
        context.push(context.vars)
        context.push(context.fp)
        context.fp = len(context.stack) # points to old fp, old vars, and return address
        context.vars = DictValue({ "result": AddressValue(None, []) })
        self.store(context, self.args, arg)
        context.pc += 1

class ReturnOp(Op):
    def __init__(self, result, default):
        self.result = result        # may be None
        self.default = default      # may be None

    def __repr__(self):
        if self.result is None:
            return "ReturnOp()"
        (lexeme, file, line, column) = self.result
        if self.default is None:
            return "ReturnOp(%s)"%lexeme
        return "ReturnOp(%s. %s)"%(lexeme, strValue(self.default))

    def jdump(self):
        if self.result is None:
            return '{ "op": "Return" }'
        (lexeme, file, line, column) = self.result
        if self.default is None:
            return '{ "op": "Return", "result": "%s" }'%lexeme
        return '{ "op": "Return", "result": "%s", "default": %s }'%(lexeme, jsonValue(self.default))

    def tladump(self):
        if self.result is None:
            return 'OpReturn(self)'
        (lexeme, file, line, column) = self.result
        if self.default is None:
            return 'OpReturnVar(self, "%s")'%lexeme
        return 'OpReturnVarDefault(self, "%s", %s)'%(lexeme, tlaValue(self.default))

    def use(self):
        if self.result is None:
            return set()
        (lexeme, file, line, column) = self.result
        return { lexeme }

    def explain(self):
        if self.result is None:
            return "restore caller method state"
        (lexeme, file, line, column) = self.result
        return "restore caller method state and push %s"%lexeme

    def eval(self, state, context):
        assert False, "obsolete"
        if len(context.stack) == 0:
            context.phase = "end"
            return
        result = context.get("result")
        context.fp = context.pop()
        context.vars = context.pop()
        context.pop()       # argument saved for stack trace
        assert isinstance(context.vars, DictValue)
        if len(context.stack) == 0:
            context.phase = "end"
            return
        calltype = context.pop()
        if calltype == "normal":
            pc = context.pop()
            assert isinstance(pc, PcValue)
            assert pc.pc != context.pc
            context.pc = pc.pc
            context.push(result)
        elif calltype == "interrupt":
            assert context.interruptLevel
            context.interruptLevel = False
            pc = context.pop()
            assert isinstance(pc, PcValue)
            assert pc.pc != context.pc
            context.pc = pc.pc
        elif calltype == "process":
            context.phase = "end"
        else:
            assert False, calltype

class SpawnOp(Op):
    def __init__(self, eternal):
        self.eternal = eternal

    def __repr__(self):
        return "Spawn"

    def jdump(self):
        return '{ "op": "Spawn", "eternal": "%s" }'%("True" if self.eternal else "False")

    def tladump(self):
        return 'OpSpawn(self)'

    def explain(self):
        return "pop thread-local state, argument, and pc and spawn a new thread"

    def eval(self, state, context):
        if context.readonly > 0:
            context.failure = "Error: no spawn allowed in assert"
            return
        this = context.pop()
        arg = context.pop()
        method = context.pop()
        assert isinstance(method, PcValue)
        frame = state.code[method.pc]
        assert isinstance(frame, FrameOp)
        ctx = ContextValue(frame.name, method.pc, arg, this)
        ctx.push("process")
        ctx.push(arg)
        bag_add(state.ctxbag, ctx)
        context.pc += 1

class TrapOp(Op):
    def __repr__(self):
        return "Trap"

    def explain(self):
        return "pop a pc and argument and set trap"

    def jdump(self):
        return '{ "op": "Trap" }'

    def tladump(self):
        return 'OpTrap(self)'

    def eval(self, state, context):
        method = context.pop()
        assert isinstance(method, PcValue)
        arg = context.pop()
        frame = state.code[method.pc]
        assert isinstance(frame, FrameOp)
        context.trap = (method, arg)
        context.pc += 1

class AtomicIncOp(Op):
    def __init__(self, lazy):
        self.lazy = lazy

    def __repr__(self):
        return "AtomicInc(%s)"%("lazy" if self.lazy else "eager")

    def tladump(self):
        return 'OpAtomicInc(self)'

    def jdump(self):
        return '{ "op": "AtomicInc", "lazy": "%s" }'%str(self.lazy)

    def explain(self):
        return "increment atomic counter of context; thread runs uninterrupted if larger than 0"

    def eval(self, state, context):
        context.atomic += 1
        context.pc += 1

class AtomicDecOp(Op):
    def __repr__(self):
        return "AtomicDec"

    def jdump(self):
        return '{ "op": "AtomicDec" }'

    def tladump(self):
        return 'OpAtomicDec(self)'

    def explain(self):
        return "decrement atomic counter of context"

    def eval(self, state, context):
        assert context.atomic > 0
        context.atomic -= 1
        context.pc += 1

class ReadonlyIncOp(Op):
    def __repr__(self):
        return "ReadonlyInc"

    def jdump(self):
        return '{ "op": "ReadonlyInc" }'

    def explain(self):
        return "increment readonly counter of context; thread cannot mutate shared variables if > 0"

    def tladump(self):
        return 'OpReadonlyInc(self)'

    def eval(self, state, context):
        context.readonly += 1
        context.pc += 1

class ReadonlyDecOp(Op):
    def __repr__(self):
        return "ReadonlyDec"

    def jdump(self):
        return '{ "op": "ReadonlyDec" }'

    def tladump(self):
        return 'OpReadonlyDec(self)'

    def explain(self):
        return "decrement readonly counter of context"

    def eval(self, state, context):
        assert context.readonly > 0
        context.readonly -= 1
        context.pc += 1

class FinallyOp(Op):
    def __init__(self, pc):
        self.pc = pc

    def __repr__(self):
        return "Finally " + str(self.pc)

    def jdump(self):
        return '{ "op": "Finally", "pc": "%d" }'%self.pc

    def tladump(self):
        return 'OpFinally(self, %d)'%(self.pc)

    def explain(self):
        return "test predicate over final state"

    def eval(self, state, context):
        assert False

    def substitute(self, map):
        if isinstance(self.pc, LabelValue):
            assert isinstance(map[self.pc], PcValue)
            self.pc = map[self.pc].pc

class InvariantOp(Op):
    def __init__(self, pc, uses_pre):
        self.pc = pc
        self.uses_pre = uses_pre        # invariant optimization

    def __repr__(self):
        return "Invariant " + str(self.pc)

    def jdump(self):
        return '{ "op": "Invariant", "pre": "%s", "pc": "%d" }'%(self.uses_pre, self.pc)

    def tladump(self):
        return 'OpInvariant(self, %s, %d)'%(self.uses_pre, self.pc)

    def explain(self):
        return "test invariant"

    def eval(self, state, context):
        assert False
        assert self.end > 0
        state.invariants |= {context.pc}
        context.pc += (self.end + 1)

    def substitute(self, map):
        if isinstance(self.pc, LabelValue):
            assert isinstance(map[self.pc], PcValue)
            self.pc = map[self.pc].pc

class JumpOp(Op):
    def __init__(self, pc, reason=None):
        self.pc = pc
        self.reason = reason

    def __repr__(self):
        return "Jump " + str(self.pc)

    def jdump(self):
        return '{ "op": "Jump", "pc": "%d" }'%self.pc

    def tladump(self):
        return 'OpJump(self, %d)'%self.pc

    def explain(self):
        prefix = "" if self.reason is None else (self.reason + ": ")
        return prefix + "set program counter to " + str(self.pc)

    def eval(self, state, context):
        assert self.pc != context.pc
        context.pc = self.pc

    def substitute(self, map):
        if isinstance(self.pc, LabelValue):
            assert isinstance(map[self.pc], PcValue)
            self.pc = map[self.pc].pc

class JumpCondOp(Op):
    def __init__(self, cond, pc, reason=None):
        self.cond = cond
        self.pc = pc
        self.reason = reason

    def __repr__(self):
        return "JumpCond " + str(self.cond) + " " + str(self.pc)

    def jdump(self):
        return '{ "op": "JumpCond", "pc": "%d", "cond": %s }'%(self.pc, jsonValue(self.cond))

    def tladump(self):
        return 'OpJumpCond(self, %d, %s)'%(self.pc, tlaValue(self.cond))

    def explain(self):
        if self.reason is None:
            prefix = ""
        else:
            prefix = self.reason + ": "
        return prefix + "pop a value and jump to " + str(self.pc) + \
            " if the value is " + strValue(self.cond)

    def eval(self, state, context):
        c = context.pop()
        if type(c) != type(self.cond):
            context.failure = "Error: incompatible types (%s, %s)"%(c, self.cond)
        elif c == self.cond:
            assert self.pc != context.pc
            context.pc = self.pc
        else:
            context.pc += 1

    def substitute(self, map):
        if isinstance(self.pc, LabelValue):
            assert isinstance(map[self.pc], PcValue)
            self.pc = map[self.pc].pc

class NaryOp(Op):
    def __init__(self, op, n):
        self.op = op
        self.n = n

    def __repr__(self):
        (lexeme, file, line, column) = self.op
        return "%d-ary "%self.n + str(lexeme)

    def jdump(self):
        (lexeme, file, line, column) = self.op
        return '{ "op": "Nary", "arity": %d, "value": "%s" }'%(self.n, lexeme)

    def tladump(self):
        (lexeme, file, line, column) = self.op
        if lexeme == "-" and self.n == 1:
            return "OpUna(self, FunMinus)"
        if lexeme == "~" and self.n == 1:
            return "OpUna(self, FunNegate)"
        if lexeme == "not" and self.n == 1:
            return "OpUna(self, FunNot)"
        if lexeme == "str" and self.n == 1:
            return "OpUna(self, FunStr)"
        if lexeme == "len" and self.n == 1:
            return "OpUna(self, FunLen)"
        if lexeme == "len" and self.n == 1:
            return "OpUna(self, FunType)"
        if lexeme == "min" and self.n == 1:
            return "OpUna(self, FunMin)"
        if lexeme == "max" and self.n == 1:
            return "OpUna(self, FunMax)"
        if lexeme == "abs" and self.n == 1:
            return "OpUna(self, FunAbs)"
        if lexeme == "any" and self.n == 1:
            return "OpUna(self, FunAny)"
        if lexeme == "all" and self.n == 1:
            return "OpUna(self, FunAll)"
        if lexeme == "keys" and self.n == 1:
            return "OpUna(self, FunKeys)"
        if lexeme == "IsEmpty" and self.n == 1:
            return "OpUna(self, FunIsEmpty)"
        if lexeme == "countLabel" and self.n == 1:
            return "OpUna(self, FunCountLabel)"
        if lexeme == "get_context" and self.n == 1:
            return "OpGetContext(self)"
        if lexeme == "get_ident" and self.n == 1:
            return "OpGetIdent(self)"
        if lexeme == ">>" and self.n == 2:
            return "OpBin(self, FunShiftRight)"
        if lexeme == "<<" and self.n == 2:
            return "OpBin(self, FunShiftLeft)"
        if lexeme == ".." and self.n == 2:
            return "OpBin(self, FunRange)"
        if lexeme == "SetAdd" and self.n == 2:
            return "OpBin(self, FunSetAdd)"
        if lexeme == "in" and self.n == 2:
            return "OpBin(self, FunIn)"
        if lexeme == "==" and self.n == 2:
            return "OpBin(self, FunEquals)"
        if lexeme == "!=" and self.n == 2:
            return "OpBin(self, FunNotEquals)"
        if lexeme == "<" and self.n == 2:
            return "OpBin(self, FunLT)"
        if lexeme == "<=" and self.n == 2:
            return "OpBin(self, FunLE)"
        if lexeme == ">" and self.n == 2:
            return "OpBin(self, FunGT)"
        if lexeme == ">=" and self.n == 2:
            return "OpBin(self, FunGE)"
        if lexeme == "-" and self.n == 2:
            return "OpBin(self, FunSubtract)"
        if lexeme == "+":
            return "OpNary(self, FunAdd, %d)"%self.n
        if lexeme == "*":
            return "OpNary(self, FunMult, %d)"%self.n
        if lexeme == "|":
            return "OpNary(self, FunUnion, %d)"%self.n
        if lexeme == "&":
            return "OpNary(self, FunIntersect, %d)"%self.n
        if lexeme == "^":
            return "OpNary(self, FunExclusion, %d)"%self.n
        if lexeme in { "/", "//" } and self.n == 2:
            return "OpBin(self, FunDiv)"
        if lexeme in { "%", "mod" } and self.n == 2:
            return "OpBin(self, FunMod)"
        if lexeme == "**" and self.n == 2:
            return "OpBin(self, FunPower)"
        if lexeme == "Closure" and self.n == 2:
            return "OpBin(self, FunClosure)"
        if lexeme == "AddArg" and self.n == 2:
            return "OpBin(self, FunAddArg)"
        if lexeme == "ListAdd" and self.n == 2:
            return "OpListAdd(self)"
        if lexeme == "DictAdd" and self.n == 3:
            return "OpDictAdd(self)"
        return 'Skip(self, "%s")'%self

    def explain(self):
        return "pop " + str(self.n) + \
            (" value" if self.n == 1 else " values") + \
            " and push the result of applying " + self.op[0]

    def atLabel(self, state, pc):
        bag: Dict[DictValue, Any] = {}
        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc == pc:
                nametag = DictValue({ 0: PcValue(ctx.entry), 1: ctx.arg })
                c = bag.get(nametag)
                bag[nametag] = cnt if c is None else (c + cnt)
        return DictValue(bag)

    def countLabel(self, state, pc):
        result = 0
        for (ctx, cnt) in state.ctxbag.items():
            if ctx.pc == pc:
                result += 1
        return result

    def contexts(self, state):
        return DictValue({ **state.ctxbag, **state.termbag, **state.stopbag })

    def concat(self, d1, d2):
        return ListValue(d1.vals + d2.vals)

    def checktype(self, state, context, args, chk):
        assert len(args) == self.n, (self, args)
        if not chk:
            context.failure = "Error: unexpected types in " + str(self.op) + \
                        " operands: " + str(list(reversed(args)))
            return False
        return True

    def checkdmult(self, state, context, args, d, e):
        if not self.checktype(state, context, args, type(e) == int):
            return False
        return True

    def dmult(self, d, e):
        return ListValue(d.vals * e)

    def eval(self, state, context):
        (op, file, line, column) = self.op
        assert len(context.stack) >= self.n, (context.stack, self.n, self.op)
        sa = context.stack[-self.n:]
        if op in { "+", "*", "&", "|", "^" }:
            assert self.n > 1
            e2 = context.pop()
            for i in range(1, self.n):
                e1 = context.pop()
                if op == "+":
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 += e1
                    elif type(e1) == str:
                        if not self.checktype(state, context, sa, type(e2) == str):
                            return
                        e2 = e1 + e2
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, ListValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, ListValue)):
                            return
                        e2 = self.concat(e1, e2)
                elif op == "*":
                    if isinstance(e1, ListValue) or isinstance(e2, ListValue):
                        if isinstance(e1, ListValue) and not self.checkdmult(state, context, sa, e1, e2):
                            return
                        if isinstance(e2, ListValue) and not self.checkdmult(state, context, sa, e2, e1):
                            return
                        e2 = self.dmult(e1, e2) if isinstance(e1, ListValue) else self.dmult(e2, e1)
                    elif isinstance(e1, str) or isinstance(e2, str):
                        if isinstance(e1, str) and not self.checktype(state, context, sa, isinstance(e2, int)):
                            return
                        if isinstance(e2, str) and not self.checktype(state, context, sa, isinstance(e1, int)):
                            return
                        e2 *= e1
                    else:
                        if not self.checktype(state, context, sa, type(e1) == int):
                            return
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 *= e1
                elif op == "&":
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 &= e1
                    elif type(e1) == SetValue:
                        if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                            return
                        e2 = SetValue(e1.s & e2.s)
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, DictValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                            return
                        d = {}
                        for (k1, v1) in e1.d.items():
                            if k1 in e2.d:
                                v2 = e2.d[k1]
                                d[k1] = v1 if keyValue(v1) < keyValue(v2) else v2
                        e2 = DictValue(d)
                elif op == "|":
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 |= e1
                    elif type(e1) == SetValue:
                        if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                            return
                        e2 = SetValue(e1.s | e2.s)
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, DictValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                            return
                        d = {}
                        for (k1, v1) in e1.d.items():
                            if k1 in e2.d:
                                v2 = e2.d[k1]
                                d[k1] = v1 if keyValue(v1) > keyValue(v2) else v2
                            else:
                                d[k1] = v1
                        for (k2, v2) in e2.d.items():
                            if k2 not in e1.d:
                                d[k2] = v2
                        e2 = DictValue(d)
                elif op == "^": 
                    if type(e1) == int:
                        if not self.checktype(state, context, sa, type(e2) == int):
                            return
                        e2 ^= e1
                    else:
                        if not self.checktype(state, context, sa, isinstance(e1, SetValue)):
                            return
                        if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                            return
                        e2 = SetValue(e2.s.union(e1.s).difference(e2.s.intersection(e1.s)))
                else:
                    assert False, op
            context.push(e2)
        elif self.n == 1:
            e = context.pop()
            if op == "-":
                if not self.checktype(state, context, sa, type(e) == int or isinstance(e, float)):
                    return
                context.push(-e)
            elif op == "~":
                if not self.checktype(state, context, sa, type(e) == int):
                    return
                context.push(~e)
            elif op == "not":
                if not self.checktype(state, context, sa, isinstance(e, bool)):
                    return
                context.push(not e)
            elif op == "abs":
                if not self.checktype(state, context, sa, type(e) == int):
                    return
                context.push(abs(e))
            elif op == "atLabel":
                if not context.atomic:
                    context.failure = "not in atomic block: " + str(self.op)
                    return
                if not self.checktype(state, context, sa, isinstance(e, PcValue)):
                    return
                context.push(self.atLabel(state, e.pc))
            elif op == "countLabel":
                if not context.atomic:
                    context.failure = "not in atomic block: " + str(self.op)
                    return
                if not self.checktype(state, context, sa, isinstance(e, PcValue)):
                    return
                context.push(self.countLabel(state, e.pc))
            elif op == "get_context":
                # if not self.checktype(state, context, sa, isinstance(e, int)):
                #   return
                context.push(context.copy())
            elif op == "get_ident":
                # if not self.checktype(state, context, sa, isinstance(e, int)):
                #   return
                assert False    # TODO
            elif op == "contexts":
                if not context.atomic:
                    context.failure = "not in atomic block: " + str(self.op)
                    return
                # if not self.checktype(state, context, sa, isinstance(e, str)):
                #     return
                context.push(self.contexts(state))
            elif op == "IsEmpty":
                if isinstance(e, DictValue):
                    context.push(e.d == {})
                elif self.checktype(state, context, sa, isinstance(e, SetValue)):
                    context.push(e.s == set())
            elif op == "min":
                if isinstance(e, DictValue):
                    if len(e.d) == 0:
                        context.failure = "Error: min() invoked with empty dict: " + str(self.op)
                    else:
                        context.push(min(e.d.values(), key=keyValue))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, SetValue)):
                        return
                    if len(e.s) == 0:
                        context.failure = "Error: min() invoked with empty set: " + str(self.op)
                    else:
                        context.push(min(e.s, key=keyValue))
            elif op == "max":
                if isinstance(e, DictValue):
                    if len(e.d) == 0:
                        context.failure = "Error: max() invoked with empty dict: " + str(self.op)
                    else:
                        context.push(max(e.d.values(), key=keyValue))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, SetValue)):
                        return
                    if len(e.s) == 0:
                        context.failure = "Error: max() invoked with empty set: " + str(self.op)
                    else:
                        context.push(max(e.s, key=keyValue))
            elif op == "len":
                if isinstance(e, SetValue):
                    context.push(len(e.s))
                elif isinstance(e, ListValue):
                    context.push(len(e.vals))
                elif isinstance(e, str):
                    context.push(len(e))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                        return
                    context.push(len(e.d))
            elif op == "type":
                if isinstance(e, bool):
                    context.push("bool")
                elif isinstance(e, int):
                    context.push("int")
                elif isinstance(e, str):
                    context.push("str")
                elif isinstance(e, PcValue):
                    context.push("pc")
                elif isinstance(e, ListValue):
                    context.push("list")
                elif isinstance(e, DictValue):
                    context.push("dict")
                elif isinstance(e, SetValue):
                    context.push("set")
                elif isinstance(e, AddressValue):
                    context.push("address")
                else:
                    assert isinstance(e, ContextValue)
                    context.push(strValue("context"))
            elif op == "str":
                context.push(strValue(e))
            elif op == "any":
                if isinstance(e, SetValue):
                    context.push(any(e.s))
                elif isinstance(e, ListValue):
                    context.push(any(e.vals))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                        return
                    context.push(any(e.d.values()))
            elif op == "all":
                if isinstance(e, SetValue):
                    context.push(all(e.s))
                elif isinstance(e, ListValue):
                    context.push(all(e.vals))
                else:
                    if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                        return
                    context.push(all(e.d.values()))
            elif op == "keys":
                if not self.checktype(state, context, sa, isinstance(e, DictValue)):
                    return
                context.push(SetValue(set(e.d.keys())))
            # elif op == "hash":
            #     context.push((e,).__hash__())
            elif op == "Closure":
                context.push(AddressValue(e, []))
            else:
                assert False, self
        elif self.n == 2:
            e2 = context.pop()
            e1 = context.pop()
            if op == "==":
                # if not self.checktype(state, context, sa, type(e1) == type(e2)):
                #     return
                context.push(e1 == e2)
            elif op == "!=":
                # if not self.checktype(state, context, sa, type(e1) == type(e2)):
                #     return
                context.push(e1 != e2)
            elif op == "<":
                context.push(keyValue(e1) < keyValue(e2))
            elif op == "<=":
                context.push(keyValue(e1) <= keyValue(e2))
            elif op == ">":
                context.push(keyValue(e1) > keyValue(e2))
            elif op == ">=":
                context.push(keyValue(e1) >= keyValue(e2))
            elif op == "-":
                if type(e1) == int or isinstance(e1, float):
                    if not self.checktype(state, context, sa, type(e2) == int or isinstance(e2, float)):
                        return
                    context.push(e1 - e2)
                else:
                    if not self.checktype(state, context, sa, isinstance(e1, SetValue)):
                        return
                    if not self.checktype(state, context, sa, isinstance(e2, SetValue)):
                        return
                    context.push(SetValue(e1.s.difference(e2.s)))
            elif op in { "/", "//" }:
                if not self.checktype(state, context, sa, type(e1) == int or isinstance(e1, float)):
                    return
                if not self.checktype(state, context, sa, type(e2) == int or isinstance(e2, float)):
                    return
                if type(e1) == int and (e2 == math.inf or e2 == -math.inf):
                    context.push(0)
                else:
                    context.push(e1 // e2)
            elif op in { "%", "mod" }:
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 % e2)
            elif op == "**":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 ** e2)
            elif op == "<<":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 << e2)
            elif op == ">>":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(e1 >> e2)
            elif op == "..":
                if not self.checktype(state, context, sa, type(e1) == int):
                    return
                if not self.checktype(state, context, sa, type(e2) == int):
                    return
                context.push(SetValue(set(range(e1, e2+1))))
            elif op == "in":
                if isinstance(e2, SetValue):
                    context.push(e1 in e2.s)
                elif isinstance(e2, str):
                    if not self.checktype(state, context, sa, isinstance(e1, str)):
                        return
                    context.push(e1 in e2)
                elif not self.checktype(state, context, sa, isinstance(e2, DictValue)):
                    return
                else:
                    context.push(e1 in e2.d)
            elif op == "SetAdd":
                assert isinstance(e1, SetValue)
                context.push(SetValue(e1.s | {e2}))
            elif op == "ListAdd":
                assert isinstance(e1, ListValue)
                context.push(ListValue(e1.vals + [e2]))
            elif op == "BagAdd":
                assert isinstance(e1, DictValue)
                d = e1.d.copy()
                if e2 in d:
                    assert isinstance(d[e2], int)
                    d[e2] += 1
                else:
                    d[e2] = 1
                context.push(DictValue(d))
            elif op == "Closure":
                context.push(AddressValue(e2, [e1]))
            else:
                assert False, self
        elif self.n == 3:
            e3 = context.pop()
            e2 = context.pop()
            e1 = context.pop()
            if op == "DictAdd":
                assert isinstance(e1, DictValue)
                d = e1.d.copy()
                if e2 in d:
                    if keyValue(d[e2]) >= keyValue(e3):
                        context.push(e1)
                    else:
                        d[e2] = e3
                        context.push(DictValue(d))
                else:
                    d[e2] = e3
                    context.push(DictValue(d))
            else:
                assert False, self
        else:
            assert False, self
        context.pc += 1
