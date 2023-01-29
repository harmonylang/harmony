from typing import Optional

class Scope:
    def __init__(self, parent: Optional['Scope']):
        self.parent = parent               # parent scope
        self.names = { "this": ("local-var", ("this", "NOFILE", 0, 0)) }   # name to (type, x) map
        self.labels: dict = {} if parent is None else parent.labels
        self.prefix: Optional[str] = None if parent is None else parent.prefix
        self.inherit = False
        self.pmap: dict = {}                  # hack for pretty-printing
        self.file = "__nofile__"              # file name
        self.uses_pre = False                 # for invariant optimization

    def copy(self):
        c = Scope(self.parent)
        c.names = self.names.copy()
        c.labels = self.labels.copy()
        c.prefix = self.prefix
        c.inherit = self.inherit
        return c

    def checkUnused(self, name):
        (lexeme, file, line, column) = name
        tv = self.names.get(lexeme)
        if tv is not None:
            (t, v) = tv
            assert t != "variable", ("variable name in use", name, v)

    def lookup(self, name):
        (lexeme, file, line, column) = name
        if lexeme == "_":
            return ("local-var", name)
        tv = self.names.get(lexeme)
        if tv is not None:
            return tv
        ancestor = self.parent
        while ancestor is not None:
            tv = ancestor.names.get(lexeme)
            if tv is not None:
                # (t, v) = tv
                # if t == "local-var":
                #    return None
                return tv
            ancestor = ancestor.parent
        # print("Warning: unknown name:", name, " (assuming global variable)")
        self.names[lexeme] = ("global", name)
        return ("global", name)

    # This is a hack to create a map of identifiers to types for
    # pretty printing.
    # TODO: come up with a better solution
    def pset(self, lexeme: str, tv):
        self.pmap[lexeme] = tv
        if self.parent is not None:
            self.parent.pset(lexeme, tv)

    def set(self, lexeme, tv):
        self.names[lexeme] = tv
        self.pset(lexeme, tv)
