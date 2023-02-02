import sys
from typing import Set, TextIO
from harmony_model_checker.harmony.ops import *
from harmony_model_checker.harmony.type_tools import Token_t, Stmt_t

class Labeled_Op:
    def __init__(self, module: str, op: Op, start: Token_t, stop: Token_t, stmt: Optional[Stmt_t], labels: Set[LabelValue]):
        self.module = module    # module
        self.op = op            # operation
        self.start = start      # first token
        self.stop = stop        # last token
        self.stmt = stmt
        self.labels = labels
        self.live_in: Set[str] = set()
        self.live_out: Set[str] = set()

class Code:
    def __init__(self, parent: Optional['Code'] = None):
        self.labeled_ops: List[Labeled_Op] = []
        self.endlabels: Set[LabelValue] = set()
        self.modstack: List[Optional[str]] = []      # module stack
        self.curModule: Optional[str] = None
        self.curFile: Optional[str] = None
        self.curLine = 0
        self.parent = parent

    def modpush(self, module: Optional[str]):
        self.modstack.append(self.curModule)
        self.curModule = module

    def modpop(self):
        self.curModule = self.modstack.pop()

    def location(self, file: str, line: int):
        self.curFile = file
        self.curLine = line

    def append(self, op: Op, start: Token_t, stop: Token_t, labels: Set[LabelValue]=set(), stmt: Optional[Stmt_t]=None):
        assert len(start) == 4
        assert len(stop) == 4
        assert self.curModule is not None
        self.labeled_ops.append(Labeled_Op(self.curModule, op, start, stop, stmt, labels | self.endlabels))
        self.endlabels = set()

    def nextLabel(self, endlabel: LabelValue):
        self.endlabels.add(endlabel)

    # This method inserts DelVar operations as soon as a variable is no
    # longer live
    def liveness(self):
        # First figure out what the labels point to and initialize
        # the nodes
        map: Dict[LabelValue, int] = {}
        lop_predecessors: Dict[int, Set[int]] = {}
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            lop_predecessors[pc] = set()
            lop.live_in = set()
            lop.live_out = set()
            for label in lop.labels:
                assert label not in map, label
                map[label] = pc
        # Compute the predecessors of each node
        for pc, lop in enumerate(self.labeled_ops):
            if isinstance(lop.op, JumpOp):
                assert isinstance(lop.op.pc, LabelValue)
                op_pc = map[lop.op.pc]
                succ = self.labeled_ops[op_pc]
                lop_predecessors[op_pc] |= {pc}
            elif isinstance(lop.op, JumpCondOp):
                assert pc < len(self.labeled_ops) - 1
                assert isinstance(lop.op.pc, LabelValue)
                op_pc = map[lop.op.pc]
                succ = self.labeled_ops[op_pc]
                lop_predecessors[op_pc] |= {pc}
                lop_predecessors[pc + 1] |= {pc}
            elif pc < len(self.labeled_ops) - 1 and not isinstance(lop.op, ReturnOp):
                lop_predecessors[pc + 1] |= {pc}
        # Live variable analysis
        change = True
        while change:
            change = False
            for pc in range(len(self.labeled_ops)):
                lop = self.labeled_ops[pc]
                if pc == len(self.labeled_ops) - 1:
                    live_out: Set[str] = set()
                elif isinstance(lop.op, JumpOp):
                    assert isinstance(lop.op.pc, LabelValue)
                    succ = self.labeled_ops[map[lop.op.pc]]
                    live_out = succ.live_in
                else:
                    live_out = self.labeled_ops[pc + 1].live_in
                    if isinstance(lop.op, JumpCondOp):
                        assert isinstance(lop.op.pc, LabelValue)
                        succ = self.labeled_ops[map[lop.op.pc]]
                        live_out = live_out | succ.live_in
                live_in = lop.op.use() | (live_out - lop.op.define())
                if not change and (live_in != lop.live_in or live_out != lop.live_out):
                    change = True
                lop.live_in = live_in
                lop.live_out = live_out
        # Create new code with DelVars inserted
        newcode = Code()
        for lop_pc, lop in enumerate(self.labeled_ops):
            # print(lop.op, lop.live_in, lop.live_out)

            # If a variable is live on output of any predecessor but not
            # live on input, delete it first
            pre_del: Set[str] = set()
            for pred in lop_predecessors[lop_pc]:
                plop = self.labeled_ops[pred]
                live_out = plop.live_out | plop.op.define()
                pre_del |= live_out - lop.live_in

            labels = lop.labels
            newcode.curModule = lop.module
            for d in sorted(pre_del - { 'this' }):
                newcode.append(DelVarOp((d, None, None, None)), lop.start, lop.stop, labels=labels, stmt=lop.stmt)
                labels = set()
            newcode.append(lop.op, lop.start, lop.stop, labels=labels, stmt=lop.stmt)

            # If a variable is defined or live on input but not live on output,
            # immediately delete afterward
            # TODO.  Can optimize StoreVar by replacing it with Pop
            # post_del = (lop.op.define() | lop.live_in) - lop.live_out
            post_del = lop.live_in - lop.live_out
            for d in sorted(post_del - { 'this' }):
                newcode.append(DelVarOp((d, None, None, None)), lop.start, lop.stop, stmt=lop.stmt)

        return newcode

    def link(self):
        map: Dict[LabelValue, PcValue] = {}
        for pc in range(len(self.labeled_ops)):
            lop = self.labeled_ops[pc]
            for label in lop.labels:
                assert label not in map, label
                map[label] = PcValue(pc)
        for lop in self.labeled_ops:
            lop.op.substitute(map)

    def dump(self, verbose: bool, f: TextIO=sys.stdout):
        import harmony_model_checker.harmony.harmony as legacy_harmony
        lastloc: Optional[Tuple[str, int]] = None
        for pc, lop in enumerate(self.labeled_ops):
            if verbose:
                file, line = self.curFile, self.curLine
                if file is not None and (file, line) != lastloc:
                    lines = legacy_harmony.files[file]
                    if lines is not None and line <= len(lines):
                        print(f"{file, line}:{lines[line-1]}", file=f)
                    else:
                        print(f"{file}:{line}", file=f)
                    lastloc = (file, line)
                print(f"  {pc} {lop}", file=f)
            else:
                print(lop, file=f)

    # Jump chaining
    def optimize(self):
        def optjump(pc: int):
            while pc < len(self.labeled_ops):
                op = self.labeled_ops[pc].op
                if not isinstance(op, JumpOp):
                    break
                pc = op.pc
            return pc

        for i, op in enumerate(self.labeled_ops):
            if isinstance(op, JumpOp):
                self.labeled_ops[i].op = JumpOp(optjump(op.pc), reason=op.reason)
            elif isinstance(op, JumpCondOp):
                self.labeled_ops[i].op = JumpCondOp(op.cond, optjump(op.pc), reason=op.reason)
