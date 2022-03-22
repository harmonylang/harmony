from typing import Union, Optional
from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor
from harmony_model_checker.harmony.ast import *


class DumpASTVisitor(AbstractASTVisitor):

    def __init__(self, indent_unit: Union[int, str] = 2):
        if isinstance(indent_unit, int):
            self.indent_unit = " " * indent_unit
        else:
            self.indent_unit = indent_unit

    def __call__(self, ast: AST, depth: Optional[int] = None):
        if depth is None:
            self.buffer = ""
            ast.accept_visitor(self, depth=0)
            return self.buffer
        else:
            ast.accept_visitor(self, depth=depth)
        
    def p(self, x, indent=0):
        self.buffer += self.indent_unit * indent + str(x) + "\n"

    def _visit_comprehension_iter(self, iter, value, depth):
        for type, rest in iter:
            if type == "for":
                _, _, expr = rest
                self(expr, depth + 1)
            
            elif type == "where":
                self(rest, depth + 1)

        self(value, depth + 1)

    def visit_constant(self, node: ConstantAST, depth):
        self.p(f"Constant {node.token}", indent=depth)

    def visit_name(self, node: NameAST, depth):
        self.p(f"Name {node.token}", indent=depth)

    def visit_set(self, node: SetAST, depth):
        self.p(f"Set {node.token}", indent=depth)

        for subnode in node.collection:
            self(subnode, depth + 1)
    
    def visit_range(self, node: RangeAST, depth):
        self.p(f"Range {node.token}", indent=depth)

        self(node.lhs, depth + 1)
        self(node.rhs, depth + 1)

    def visit_tuple(self, node: TupleAST, depth):
        self.p(f"Tuple {node.token}", indent=depth)

        for subnode in node.list:
            self(subnode, depth + 1)

    def visit_dict(self, node: DictAST, depth):
        self.p(f"Dict {node.token}", indent=depth)

        for (k, v) in node.record:
            self(k, depth + 1)
            self(v, depth + 1)

    def visit_set_comprehension(self, node: SetComprehensionAST, depth):
        self.p(f"SetComprehension {node.token}", indent=depth)

        self._visit_comprehension_iter(node.iter, node.value, depth)

    def visit_dict_comprehension(self, node: DictComprehensionAST, depth):
        self.p(f"DictComprehension {node.token}", indent=depth)

        self._visit_comprehension_iter(node.iter, node.value, depth)

    def visit_list_comprehension(self, node: ListComprehensionAST, depth):
        self.p(f"ListComprehension {node.token}", indent=depth)

        self._visit_comprehension_iter(node.iter, node.value, depth)

    def visit_nary(self, node: NaryAST, depth):
        self.p(f"Nary {node.token}", indent=depth)

        for subnode in node.args:
            self(subnode, depth + 1)

    def visit_cmp(self, node: CmpAST, depth):
        self.p(f"Cmp {node.token}", indent=depth)

        for subnode in node.args:
            self(subnode, depth + 1)

    def visit_apply(self, node: ApplyAST, depth):
        self.p(f"Apply {node.token}", indent=depth)

        self(node.arg, depth + 1)

    def visit_pointer(self, node: PointerAST, depth):
        self.p(f"Pointer {node.token}", indent=depth)

        self(node.expr, depth + 1)

    def visit_assignment(self, node: AssignmentAST, depth):
        self.p(f"Assignment {node.token}", indent=depth)

        for lhs in node.lhslist:
            self(lhs, depth + 1)

        self(node.rv, depth + 1)

    def visit_del(self, node: DelAST, depth):
        self.p(f"Del {node.token}", indent=depth)

    def visit_set_int_level(self, node: SetIntLevelAST, depth):
        self.p(f"SetIntLevel {node.token}", indent=depth)

    def visit_save(self, node: SaveAST, depth):
        self.p(f"Save {node.token}", indent=depth)

    def visit_stop(self, node: StopAST, depth):
        self.p(f"Stop {node.token}", indent=depth)

    def visit_address(self, node: AddressAST, depth):
        self.p(f"Address {node.token}", indent=depth)

        self(node.lv, depth + 1)

    def visit_pass(self, node: PassAST, depth):
        self.p(f"Pass {node.token}", indent=depth)

    def visit_block(self, node: BlockAST, depth):
        self.p(f"Block {node.token}", indent=depth)

        for subnode in node.b:
            self(subnode, depth + 1)

    def visit_if(self, node: IfAST, depth):
        self.p(f"If {node.token}", indent=depth)

        for alt in node.alts:
            _, stat, _, _ = alt 
            self(stat, depth + 1)

        if node.stat is not None:
            self(node.stat, depth + 1)

    def visit_while(self, node: WhileAST, depth):
        self.p(f"While {node.token}", indent=depth)

        self(node.cond, depth + 1)
        self(node.stat, depth + 1)

    def visit_invariant(self, node: InvariantAST, depth):
        self.p(f"Invariant {node.token}", indent=depth)

        self(node.cond, depth + 1)

    def visit_let(self, node: LetAST, depth):
        self.p(f"Let {node.token}", indent=depth)

        for _, expr in node.vars:
            self(expr, depth + 1)

        self(node.stat, depth + 1)

    def visit_var(self, node: VarAST, depth):
        self.p(f"Var {node.token}", indent=depth)

        for _, expr in node.vars:
            self(expr, depth + 1)

    def visit_for(self, node: ForAST, depth):
        self.p(f"For {node.token}", indent=depth)

        self._visit_comprehension_iter(node.iter, node.value, depth)
    
    def visit_let_when(self, node: LetWhenAST, depth):
        self.p(f"LetWhen {node.token}", indent=depth)

        for var_or_cond in node.vars_and_conds:
            if var_or_cond[0] == 'var':
                _, expr = var_or_cond[1:]
                self(expr, depth + 1)

            elif var_or_cond[0] == 'cond':
                cond = var_or_cond[1]
                self(cond, depth + 1)
        
    def visit_atomic(self, node: AtomicAST, depth):
        self.p(f"Atomic {node.token}", indent=depth)

        self(node.stat, depth + 1)

    def visit_assert(self, node: AssertAST, depth):
        self.p(f"Assert {node.token}", indent=depth)

        self(node.cond, depth + 1)

        if node.expr is not None:
            self(node.expr, depth + 1)

    def visit_print(self, node: PrintAST, depth):
        self.p(f"Print {node.token}", indent=depth)

        self(node.expr, depth + 1)

    def visit_method(self, node: MethodAST, depth):
        self.p(f"Method {node.token}", indent=depth)

        self(node.stat, depth + 1)

    def visit_lambda(self, node: LambdaAST, depth):
        self.p(f"Lambda {node.token}", indent=depth)

        self(node.stat, depth + 1)

    def visit_call(self, node: CallAST, depth):
        self.p(f"Call {node.token}", indent=depth)

        self(node.expr, depth + 1)

    def visit_spawn(self, node: SpawnAST, depth):
        self.p(f"Spawn {node.token}", indent=depth)

        self(node.method, depth + 1)
        self(node.arg, depth + 1)

    def visit_trap(self, node: TrapAST, depth):
        self.p(f"Trap {node.token}", indent=depth)

        self(node.arg, depth + 1)
        self(node.method, depth + 1)

    def visit_go(self, node: GoAST, depth):
        self.p(f"Go {node.token}", indent=depth)

    def visit_import(self, node: ImportAST, depth):
        self.p(f"Import {node.token}", indent=depth)

    def visit_from(self, node: FromAST, depth):
        self.p(f"From {node.token}", indent=depth)

    def visit_location(self, node: LocationAST, depth):
        self.p(f"Location {node.token}", indent=depth)

        self(node.ast, depth + 1)

    def visit_label_stat(self, node: LabelStatAST, depth):
        self.p(f"LabelStat {node.token}", indent=depth)

    def visit_sequential(self, node: SequentialAST, depth):
        self.p(f"Sequential {node.token}", indent=depth)

    def visit_const(self, node: ConstAST, depth):
        self.p(f"Const {node.token}", indent=depth)
