import json

tlavarcnt = 0           # to generate unique TLA+ variables

def tlaValue(lexeme):
    if isinstance(lexeme, bool):
        return 'HBool(%s)'%("TRUE" if lexeme else "FALSE")
    if isinstance(lexeme, int):
        return 'HInt(%d)'%lexeme
    if isinstance(lexeme, str):
        return 'HStr("%s")'%lexeme
    return lexeme.tlaval()

def strValue(v):
    if isinstance(v, Value) or isinstance(v, bool) or isinstance(v, int) or isinstance(v, float):
        return str(v)
    if isinstance(v, str):
        return '"%s"'%v
    assert False, v

def jsonValue(v):
    if isinstance(v, Value):
        return v.jdump()
    if isinstance(v, bool):
        return '{ "type": "bool", "value": "%s" }'%str(v)
    if isinstance(v, int) or isinstance(v, float):
        return '{ "type": "int", "value": %s }'%str(v)
    if isinstance(v, str):
        return '{ "type": "atom", "value": %s }'%json.dumps(v, ensure_ascii=False)
    assert False, v

def strVars(v):
    assert isinstance(v, DictValue)
    result = ""
    for (var, val) in v.d.items():
        if result != "":
            result += ", "
        result += strValue(var)[1:] + "=" + strValue(val)
    return "{" + result + "}"

def keyValue(v):
    if isinstance(v, bool):
        return (0, v)
    if isinstance(v, int):
        return (1, v)
    if isinstance(v, str):
        return (2, v)
    assert isinstance(v, Value), v
    return v.key()

def substValue(v, map):
    return v.substitute(map) if isinstance(v, Value) else v

class Value:
    def __str__(self):
        return self.__repr__()

    def jdump(self):
        assert False

    def substitute(self, map):
        assert False, self

class PcValue(Value):
    def __init__(self, pc):
        assert isinstance(pc, int), pc
        self.pc = pc

    def __repr__(self):
        return "PC(" + str(self.pc) + ")"

    def tlaval(self):
        return 'HPc(%d)'%self.pc

    def __hash__(self):
        return self.pc.__hash__()

    def __eq__(self, other):
        return isinstance(other, PcValue) and other.pc == self.pc

    def key(self):
        return (3, self.pc)

    def jdump(self):
        return '{ "type": "pc", "value": "%d" }'%self.pc

    def substitute(self, map):
        # return substValue(self.pc, map)
        return self

class _LabelIdGenerator:

    _next_id = 0

    @classmethod
    def new_id(cls):
        result = cls._next_id
        cls._next_id += 1
        return result

# This is a substitute for PCValues used before values are assigned to labels
# TODO.  Get rid of all but id
class LabelValue(Value):

    def __init__(self, module, label):
        self.id = _LabelIdGenerator.new_id()
        self.module = module
        self.label = label

    def __repr__(self):
        if self.module == None:
            return "LABEL(" + str(self.id) + ", " + self.label + ")"
        else:
            return "LABEL(" + self.module + ":" + self.label + ")"

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, LabelValue) and other.id == self.id

    def key(self):
        return (100, self.id)

    def jdump(self):
        assert False

    def substitute(self, map):
        return map[self] if self in map else self

class ListValue(Value):
    def __init__(self, vals):
        self.vals = vals

    def __repr__(self):
        if self.vals == []:
            return "()"
        result = ""
        for v in self.vals:
            if result != "":
                result += ", "
            result += strValue(v)
        if len(self.vals) == 1:
            result += ","
        return "[" + result + "]"

    def tlaval(self):
        s = "<<" + ",".join(tlaValue(x) for x in self.vals) + ">>"
        return 'HList(%s)'%s

    def jdump(self):
        result = ""
        for v in self.vals:
            if result != "":
                result += ", "
            result += jsonValue(v)
        return '{ "type": "list", "value": [%s] }'%result

    def __hash__(self):
        hash = 0
        for v in self.vals:
            hash ^= v.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, ListValue):
            return False
        return self.vals == other.vals

    def __len__(self):
        return len(self.vals)

    def key(self):
        return (4, [ keyValue(v) for v in self.vals ])

    def substitute(self, map):
        return ListValue([ substValue(v, map) for v in self.vals ])

class DictValue(Value):
    def __init__(self, d):
        self.d = d

    def __repr__(self):
        if len(self.d) == 0:
            return "{:}"
        result = ""
        if set(self.d.keys()) == set(range(len(self.d))):
            for k in range(len(self.d)):
                if result != "":
                    result += ", "
                result += strValue(self.d[k])
            return "[" + result + "]"
        keys = sorted(self.d.keys(), key=keyValue)
        for k in keys:
            if result != "":
                result += ", "
            result += strValue(k) + ":" + strValue(self.d[k])
        return "{ " + result + " }"

    def tlaval(self):
        global tlavarcnt

        tlavar = "x%d"%tlavarcnt
        tlavarcnt += 1
        if len(self.d) == 0:
            return 'EmptyDict'
        s = "[ %s \\in {"%tlavar + ",".join({ tlaValue(k) for k in self.d.keys() }) + "} |-> "
        # special case: all values are the same
        vals = list(self.d.values())
        if vals.count(vals[0]) == len(vals):
            s += tlaValue(vals[0]) + " ]"
            return 'HDict(%s)'%s

        # not all values are the same
        first = True
        for k,v in self.d.items():
            if first:
                s += "CASE "
                first = False
            else:
                s += " [] "
            s += "%s = "%tlavar + tlaValue(k) + " -> " + tlaValue(v)
        s += " [] OTHER -> FALSE ]"
        return 'HDict(%s)'%s

    def jdump(self):
        result = ""
        keys = sorted(self.d.keys(), key=keyValue)
        for k in keys:
            if result != "":
                result += ", "
            result += '{ "key": %s, "value": %s }'%(jsonValue(k), jsonValue(self.d[k]))
        return '{ "type": "dict", "value": [%s] }'%result

    def __hash__(self):
        hash = 0
        for x in self.d.items():
            hash ^= x.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, DictValue):
            return False
        return self.d == other.d

    def __len__(self):
        return len(self.d)

    # Dictionary ordering generalizes lexicographical ordering when the dictionary
    # represents a list or tuple
    def key(self):
        return (5, [ (keyValue(v), keyValue(self.d[v]))
                        for v in sorted(self.d.keys(), key=keyValue)])

    def substitute(self, map):
        return DictValue({ substValue(k, map): substValue(v, map)
                            for (k, v) in self.d.items() })

emptytuple = ListValue([])
emptydict = DictValue({})

class SetValue(Value):
    def __init__(self, s):
        self.s = s

    def __repr__(self):
        if len(self.s) == 0:
            return "{}"
        result = ""
        vals = sorted(self.s, key=keyValue)
        for v in vals:
            if result != "":
                result += ", "
            result += strValue(v)
        return "{ " + result + " }"

    def tlaval(self):
        s = "{" + ",".join(tlaValue(x) for x in self.s) + "}"
        return 'HSet(%s)'%s

    def jdump(self):
        result = ""
        vals = sorted(self.s, key=keyValue)
        for v in vals:
            if result != "":
                result += ", "
            result += jsonValue(v)
        return '{ "type": "set", "value": [%s] }'%result

    def __hash__(self):
        return frozenset(self.s).__hash__()

    def __eq__(self, other):
        if not isinstance(other, SetValue):
            return False
        return self.s == other.s

    def key(self):
        return (6, [keyValue(v) for v in sorted(self.s, key=keyValue)])

    def substitute(self, map):
        return SetValue({ substValue(v, map) for v in self.s })

# An address is a closure consisting of a function and a list of arguments
# All are of type Value.  Due to backwards compatibility, we also have to
# represent "None" as an AddressValue.  For this we use func=None and args=[].
class AddressValue(Value):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def remainder(self):
        result = ""
        for index in self.args[1:]:
            result += "[" + strValue(index) + "]"
        return result

    def __repr__(self):
        if self.func == None:
            assert self.args == []
            return "None"
        assert self.args != []
        if isinstance(self.func, PcValue):
            if self.func.pc in { -1, -2 }:      # shared or method variable
                return "?" + self.args[0] + self.remainder()
            if self.func.pc == -3:              # thread-local variable
                return "?this." + self.args[0] + self.remainder()
        return "?" + strValue(self.args[0]) + self.remainder()

    def tlaval(self):
        s = "<<" + ",".join(tlaValue(x) for x in self.args) + ">>"
        return 'Address(%s, %s)'%(tlaValue(self.func), s)

    def jdump(self):
        if self.func == None:
            return '{ "type": "address" }'
        result = ""
        for index in self.args:
            if result != "":
                result += ", "
            result = result + jsonValue(index)
        return '{ "type": "address", "func": %s, "args": [%s] }'%(jsonValue(self.func), result)

    def __hash__(self):
        hash = 0
        for x in self.args:
            hash ^= x.__hash__()
        return hash

    def __eq__(self, other):
        if not isinstance(other, AddressValue):
            return False
        return self.args == other.args

    def key(self):
        return (7, self.args)

    def substitute(self, map):
        return AddressValue(substValue(self.func, map), [ substValue(v, map) for v in self.args ])

class ContextValue(Value):
    def __init__(self, name, entry, arg, this):
        self.name = name
        self.entry = entry
        self.arg = arg
        self.pc = entry
        self.this = this
        self.atomic = 0
        self.readonly = 0
        self.interruptLevel = False
        self.stack = []     # collections.deque() seems slightly slower
        self.fp = 0         # frame pointer
        self.vars = emptydict
        self.trap = None
        self.phase = "start"        # start, middle, or end
        self.stopped = False
        self.failure = None

    def __repr__(self):
        return "ContextValue(" + str(self.name) + ", " + str(self.arg) + ", " + str(self.this) + ")"

    def __str__(self):
        return self.__repr__()

    def nametag(self):
        if self.arg == emptytuple:
            return self.name[0] + "()"
        return self.name[0] + "(" + str(self.arg) + ")"

    def __hash__(self):
        h = (self.name, self.entry, self.arg, self.pc, self.this, self.atomic, self.readonly, self.interruptLevel, self.vars,
            self.trap, self.phase, self.stopped, self.failure).__hash__()
        for v in self.stack:
            h ^= v.__hash__()
        return h

    def __eq__(self, other):
        if not isinstance(other, ContextValue):
            return False
        if self.name != other.name:
            return False
        if self.entry != other.entry:
            return False
        if self.arg != other.arg:
            return False
        if self.pc != other.pc:
            return False
        if self.this != other.this:
            return False
        if self.atomic != other.atomic:
            return False
        if self.readonly != other.readonly:
            return False
        if self.interruptLevel != other.interruptLevel:
            return False
        if self.phase != other.phase:
            return False
        if self.stopped != other.stopped:
            return False
        if self.fp != other.fp:
            return False
        if self.trap != other.trap:
            return False
        if self.failure != other.failure:
            return False
        return self.stack == other.stack and self.vars == other.vars

    def copy(self):
        c = ContextValue(self.name, self.entry, self.arg, self.this)
        c.pc = self.pc
        c.atomic = self.atomic
        c.readonly = self.readonly
        c.interruptLevel = self.interruptLevel
        c.stack = self.stack.copy()
        c.fp = self.fp
        c.trap = self.trap
        c.vars = self.vars
        c.phase = self.phase
        c.stopped = self.stopped
        c.failure = self.failure
        return c

    def get(self, var):
        return self.this if var == "this" else self.vars.d[var]

    def iget(self, indexes):
        assert indexes[0] != "this"
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

    def doDelete(self, record, indexes):
        if len(indexes) > 1:
            d = record.d.copy()
            d[indexes[0]] = self.doDelete(record.d[indexes[0]], indexes[1:])
        else:
            d = record.d.copy()
            if indexes[0] in d:
                del d[indexes[0]]
        return DictValue(d)

    def set(self, indexes, val):
        if indexes[0] == "this":
            if len(indexes) == 1:
                self.this = val
            else:
                self.this = self.update(self.this, indexes[1:], val)
        else:
            self.vars = self.update(self.vars, indexes, val)

    def delete(self, indexes):
        self.vars = self.doDelete(self.vars, indexes)

    def push(self, val):
        assert val != None
        self.stack.append(val)

    def pop(self):
        return self.stack.pop()

    def key(self):
        return (8, (self.pc, self.__hash__()))
