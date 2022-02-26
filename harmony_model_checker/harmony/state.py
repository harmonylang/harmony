import sys
from harmony_model_checker.harmony.value import novalue, DictValue


class State:

    def __init__(self, code, labels):
        self.code = code
        self.labels = labels
        self.vars = novalue
        self.ctxbag = {}        # running contexts
        self.stopbag = {}       # stopped contexts
        self.termbag = {}       # terminated contexts
        self.choosing = None
        self.invariants = set()
        self.initializing = True

    def __repr__(self):
        return "State(" + str(self.vars) + ", " + str(self.ctxbag) + ", " + \
               str(self.stopbag) + ", " + str(self.invariants) + ")"

    def __hash__(self):
        h = self.vars.__hash__()
        for c in self.ctxbag.items():
            h ^= c.__hash__()
        for c in self.stopbag.items():
            h ^= c.__hash__()
        for c in self.termbag.items():
            h ^= c.__hash__()
        for i in self.invariants:
            h ^= i
        return h

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        assert self.code == other.code and self.labels == other.labels
        if self.vars != other.vars:
            return False
        if self.ctxbag != other.ctxbag:
            return False
        if self.stopbag != other.stopbag:
            return False
        if self.termbag != other.termbag:
            return False
        if self.choosing != other.choosing:
            return False
        if self.invariants != other.invariants:
            return False
        if self.initializing != self.initializing:
            return False
        return True

    def copy(self):
        s = State(self.code, self.labels)
        s.vars = self.vars      # no need to copy as store operations do it
        s.ctxbag = self.ctxbag.copy()
        s.stopbag = self.stopbag.copy()
        s.termbag = self.termbag.copy()
        s.choosing = self.choosing
        s.invariants = self.invariants.copy()
        s.initializing = self.initializing
        return s

    def get(self, var):
        return self.vars.d[var]

    def iget(self, indexes):
        path = indexes
        v = self.vars
        while indexes != []:
            try:
                v = v.d[indexes[0]]
            except KeyError:
                print()
                print("no index", indexes[0], "in variable", path)
                sys.exit(1)
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
        d = record.d.copy()
        if len(indexes) > 1:
            d[indexes[0]] = self.doDelete(record.d[indexes[0]], indexes[1:])
        else:
            del d[indexes[0]]
        return DictValue(d)

    def doStop(self, record, indexes, ctx):
        d = record.d.copy()
        if len(indexes) > 1:
            d[indexes[0]] = self.doStop(record.d[indexes[0]], indexes[1:], ctx)
        else:
            # TODO.  Should be print + set failure
            list = d[indexes[0]]
            assert(isinstance(list, DictValue))
            d2 = list.d.copy()
            d2[len(d2)] = ctx
            d[indexes[0]] = DictValue(d2)
        return DictValue(d)

    def set(self, indexes, val):
        self.vars = self.update(self.vars, indexes, val)

    def delete(self, indexes):
        self.vars = self.doDelete(self.vars, indexes)

    def stop(self, indexes, ctx):
        self.vars = self.doStop(self.vars, indexes, ctx)
        cnt = self.stopbag.get(ctx)
        if cnt == None:
            self.stopbag[ctx] = 1
        else:
            self.stopbag[ctx] = cnt + 1

