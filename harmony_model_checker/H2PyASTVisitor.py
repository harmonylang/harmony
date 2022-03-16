from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor

import harmony_model_checker.harmony.ast as hast  # hast = Harmony AST
import ast as past  # past = Python AST


# Symbolic constants for indexing into a token.
T_TOKEN = 0
T_FILE = 1
T_LINENO = 2
T_COLNO = 3


class H2PyASTVisitor(AbstractASTVisitor):

    def __call__(self, node: hast.AST, **kwargs) -> past.AST:
        return node.accept_visitor(self, **kwargs)

    def visit_block(self, node: hast.BlockAST, wrap_in_module: bool = True, **kwargs):
        return past.Module(
            body=[self(child, **kwargs) for child in node.b],
            type_ignores=[]
        )

    def visit_location(self, node: hast.LocationAST, **kwargs):
        return self(node.ast, **kwargs)

    # TODO: handle hast.AssignmentAST.op
    def visit_assignment(self, node: hast.AssignmentAST, **kwargs):
        def convert_targets(targets):
            if isinstance(targets, list):
                return [convert_targets(target) for target in targets]
            elif isinstance(targets, hast.TupleAST):
                return past.Tuple(
                    elts=[convert_targets(target) for target in targets.list],
                    ctx=past.Store()
                )
            elif isinstance(targets, hast.NameAST):
                return past.Name(
                    id=targets.name[0],
                    ctx=past.Store()
                )
            else:
                assert False, targets

        return past.Assign(
            targets=convert_targets(node.lhslist),
            value=self(node.rv, ctx=past.Load(), **kwargs),
            lineno=node.token[T_LINENO]
        )

    def visit_name(self, node: hast.NameAST, ctx, **kwargs):
        return past.Name(id=node.name[T_TOKEN], ctx=ctx)

    def visit_nary(self, node: hast.NaryAST, **kwargs):
        op = node.op[T_TOKEN]
        if op == '+':
            return past.BinOp(
                left=self(node.args[0], **kwargs),
                op=past.Add(),
                right=self(node.args[1], **kwargs)
            )

        elif op == "*":
            return past.BinOp(
                left=self(node.args[0], **kwargs),
                op=past.Mult(),
                right=self(node.args[1], **kwargs)
            )

        elif op == "-":
            return past.BinOp(
                left=self(node.args[0], **kwargs),
                op=past.Sub(),
                right=self(node.args[1], **kwargs)
            )

        else:
            raise NotImplementedError(op)

    def visit_constant(self, node: hast.ConstantAST, **kwargs):
        return past.Constant(value=node.const[T_TOKEN])

    def visit_print(self, node: hast.PrintAST, **kwargs):
        return past.Expr(
            value=past.Call(
                func=past.Name(id='print', ctx=past.Load()),
                args=[self(node.expr, ctx=past.Load(), **kwargs)],
                keywords=[]
            )
        )

    # TODO: Smartly add function prologue and epilogue
    def visit_method(self, node: hast.MethodAST, **kwargs):
        def convert_parameters(parameters):
            if isinstance(parameters, tuple):
                return [past.arg(arg=parameters[T_TOKEN])]
            elif isinstance(parameters, list):
                return [past.arg(arg=arg[T_TOKEN]) for arg in parameters]

        return past.FunctionDef(
            name=node.name[T_TOKEN],
            args=past.arguments(
                posonlyargs=[],
                args=convert_parameters(node.args),
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[]
            ),
            body=[
                past.Assign(
                    targets=[past.Name(id="result", ctx=past.Store())],
                    value=past.Constant(value=None),
                    lineno=node.token[T_LINENO]
                ),
                self(node.stat, **kwargs),
                past.Return(
                    value=past.Name(id="result", ctx=past.Load())
                )
            ],
            decorator_list=[],
            lineno=node.token[T_LINENO]
        )

    def visit_call(self, node: hast.CallAST, **kwargs):
        return self(node.expr, **kwargs)

    # TODO: what if apply is on a dictionary?
    def visit_apply(self, node: hast.ApplyAST, **kwargs):
        def convert_arg(arg):
            if isinstance(arg, list):
                result = []
                for subarg in arg:
                    result += convert_arg(subarg)
                return result

            elif isinstance(arg, hast.TupleAST):
                return convert_arg(arg.list)

            elif isinstance(arg, hast.ConstantAST):
                return [past.Constant(value=arg.const[0])]

            else:
                assert False, arg

        if isinstance(node.method, hast.NameAST):
            return past.Expr(
                value=past.Call(
                    func=past.Name(id=node.method.name[T_TOKEN], ctx=past.Load()),
                    args=convert_arg(node.arg),
                    keywords=[]
                )
            )

    def visit_tuple(self, node: hast.TupleAST, ctx, **kwargs):
        return past.Tuple(
            elts=[self(subnode, ctx=ctx, **kwargs) for subnode in node.list],
            ctx=ctx
        )

    def visit_assert(self, node: hast.AssertAST, **kwargs):
        return past.Assert(
            test=self(node.cond, **kwargs)
        )

    def visit_cmp(self, node: hast.CmpAST, **kwargs):
        assert len(node.ops) == 1

        op = node.ops[0][T_TOKEN]
        if op == "==":
            return past.Compare(
                left=self(node.args[0], **kwargs),
                ops=[past.Eq()],
                comparators=[self(node.args[1], **kwargs)]
            )

        else:
            raise NotImplementedError()

    def visit_let(self, node: hast.LetAST, **kwargs):
        stmts = []
        for var, expr in node.vars:
            stmts.append(past.Assign(
                targets=[past.Name(id=var[T_TOKEN], ctx=past.Store())],
                value=self(expr, ctx=past.Load(), **kwargs),
                lineno=node.token[T_LINENO]
            ))

        stmts.append(self(node.stat, **kwargs))

        for var, _ in node.vars:
            stmts.append(past.Assign(
                targets=[past.Name(id=var[T_TOKEN], ctx=past.Store())],
                value=past.Constant(value=None),
                lineno=node.token[T_LINENO]
            ))

        return stmts
