from harmony_model_checker.harmony.ast import *


class AbstractASTVisitor:

    def visit_constant(self, node: ConstantAST, *args, **kwargs):
        pass

    def visit_name(self, node: NameAST, *args, **kwargs):
        pass

    def visit_set(self, node: SetAST, *args, **kwargs):
        pass

    def visit_range(self, node: RangeAST, *args, **kwargs):
        pass

    def visit_tuple(self, node: TupleAST, *args, **kwargs):
        pass

    def visit_dict(self, node: DictAST, *args, **kwargs):
        pass

    def visit_set_comprehension(self, node: SetComprehensionAST, *args, **kwargs):
        pass

    def visit_dict_comprehension(self, node: DictComprehensionAST, *args, **kwargs):
        pass

    def visit_list_comprehension(self, node: ListComprehensionAST, *args, **kwargs):
        pass

    def visit_nary(self, node: NaryAST, *args, **kwargs):
        pass

    def visit_cmp(self, node: CmpAST, *args, **kwargs):
        pass

    def visit_apply(self, node: ApplyAST, *args, **kwargs):
        pass

    def visit_pointer(self, node: PointerAST, *args, **kwargs):
        pass

    def visit_assignment(self, node: AssignmentAST, *args, **kwargs):
        pass

    def visit_del(self, node: DelAST, *args, **kwargs):
        pass

    def visit_set_int_level(self, node: SetIntLevelAST, *args, **kwargs):
        pass

    def visit_save(self, node: SaveAST, *args, **kwargs):
        pass

    def visit_stop(self, node: StopAST, *args, **kwargs):
        pass

    def visit_address(self, node: AddressAST, *args, **kwargs):
        pass

    def visit_pass(self, node: PassAST, *args, **kwargs):
        pass

    def visit_block(self, node: BlockAST, *args, **kwargs):
        pass

    def visit_if(self, node: IfAST, *args, **kwargs):
        pass

    def visit_while(self, node: WhileAST, *args, **kwargs):
        pass

    def visit_invariant(self, node: InvariantAST, *args, **kwargs):
        pass

    def visit_let(self, node: LetAST, *args, **kwargs):
        pass

    def visit_var(self, node: VarAST, *args, **kwargs):
        pass

    def visit_for(self, node: ForAST, *args, **kwargs):
        pass

    def visit_let_when(self, node: LetWhenAST, *args, **kwargs):
        pass

    def visit_atomic(self, node: AtomicAST, *args, **kwargs):
        pass

    def visit_assert(self, node: AssertAST, *args, **kwargs):
        pass

    def visit_print(self, node: PrintAST, *args, **kwargs):
        pass

    def visit_method(self, node: MethodAST, *args, **kwargs):
        pass

    def visit_lambda(self, node: LambdaAST, *args, **kwargs):
        pass

    def visit_call(self, node: CallAST, *args, **kwargs):
        pass

    def visit_spawn(self, node: SpawnAST, *args, **kwargs):
        pass

    def visit_trap(self, node: TrapAST, *args, **kwargs):
        pass

    def visit_go(self, node: GoAST, *args, **kwargs):
        pass

    def visit_import(self, node: ImportAST, *args, **kwargs):
        pass

    def visit_from(self, node: FromAST, *args, **kwargs):
        pass

    def visit_location(self, node: LocationAST, *args, **kwargs):
        pass 

    def visit_label_stat(self, node: LabelStatAST, *args, **kwargs):
        pass

    def visit_sequential(self, node: SequentialAST, *args, **kwargs):
        pass

    def visit_const(self, node: ConstAST, *args, **kwargs):
        pass
