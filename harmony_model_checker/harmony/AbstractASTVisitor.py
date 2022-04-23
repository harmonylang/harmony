from harmony_model_checker.harmony.ast import *


class AbstractASTVisitor:

    def _not_implemented(self, node, *args, **kwargs):
        raise NotImplementedError(f'Not implemented: {type(node)}')

    def visit_constant(self, node: ConstantAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_name(self, node: NameAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_set(self, node: SetAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_range(self, node: RangeAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_tuple(self, node: TupleAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_dict(self, node: DictAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_set_comprehension(self, node: SetComprehensionAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_dict_comprehension(self, node: DictComprehensionAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_list_comprehension(self, node: ListComprehensionAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_nary(self, node: NaryAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_cmp(self, node: CmpAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_apply(self, node: ApplyAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_pointer(self, node: PointerAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_assignment(self, node: AssignmentAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_del(self, node: DelAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_set_int_level(self, node: SetIntLevelAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_save(self, node: SaveAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_stop(self, node: StopAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_address(self, node: AddressAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_pass(self, node: PassAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_block(self, node: BlockAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_if(self, node: IfAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_while(self, node: WhileAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_invariant(self, node: InvariantAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_let(self, node: LetAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_var(self, node: VarAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_for(self, node: ForAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_let_when(self, node: LetWhenAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_atomic(self, node: AtomicAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_assert(self, node: AssertAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_print(self, node: PrintAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_method(self, node: MethodAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_lambda(self, node: LambdaAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_call(self, node: CallAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_spawn(self, node: SpawnAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_trap(self, node: TrapAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_go(self, node: GoAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_import(self, node: ImportAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_from(self, node: FromAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_location(self, node: LocationAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_label_stat(self, node: LabelStatAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_sequential(self, node: SequentialAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)

    def visit_const(self, node: ConstAST, *args, **kwargs):
        self._not_implemented(node, *args, **kwargs)
