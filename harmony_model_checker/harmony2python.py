import sys

from harmony_model_checker.compile import parse
from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor
from harmony_model_checker.harmony.DumpASTVisitor import DumpASTVisitor

import harmony_model_checker.harmony.ast as hast # hast = Harmony AST
import ast as past # past = Python AST


class H2PyASTVisitor(AbstractASTVisitor):

    def __call__(self, node: hast.AST, **kwargs) -> past.AST:
        return node.accept_visitor(self, **kwargs)

    def visit_block(self, node: hast.BlockAST, wrap_in_module: bool = True, **kwargs):
        body = [self(child, **kwargs) for child in node.b]

        if wrap_in_module:
            return past.Module(
                body=body,
                type_ignores=[]
            )

        else:
            return body

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
            lineno=node.token[2]
        )

    def visit_name(self, node: hast.NameAST, ctx, **kwargs):
        return past.Name(id=node.name[0], ctx=ctx)

    def visit_nary(self, node: hast.NaryAST, **kwargs):
        op = node.op[0]
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
        return past.Constant(value=node.const[0])

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
                return past.arg(arg=parameters[0])
            elif isinstance(parameters, list):
                return [convert_parameters(arg) for arg in parameters]

        return past.FunctionDef(
            name=node.name[0],
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
                    lineno=node.token[2]
                ),
                *self(node.stat, wrap_in_module=False, **kwargs),
                past.Return(
                    value=past.Name(id="result", ctx=past.Load())
                )
            ],
            decorator_list=[],
            lineno=node.token[2]
        )

    def visit_call(self, node: hast.CallAST, **kwargs):
        return self(node.expr, **kwargs)

    # TODO: what if apply is on a dictionary?
    def visit_apply(self, node: hast.ApplyAST, **kwargs):
        def convert_arg(arg):
            if isinstance(arg, list):
                return [convert_arg(subarg) for subarg in arg]

            elif isinstance(arg, hast.TupleAST):
                return [convert_arg(subarg) for subarg in arg.list]

            elif isinstance(arg, hast.ConstantAST):
                return past.Constant(value=arg.const[0])

            else:
                assert False, arg

        if isinstance(node.method, hast.NameAST):
            return past.Expr(
                value=past.Call(
                    func=past.Name(id=node.method.name[0], ctx=past.Load()),
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

        op = node.ops[0][0]
        if op == "==":
            return past.Compare(
                left=self(node.args[0], **kwargs),
                ops=[past.Eq()],
                comparators=[self(node.args[1], **kwargs)]
            )

        else:
            raise NotImplementedError()


h2py = H2PyASTVisitor()
dump_ast = DumpASTVisitor()


def main():
    ast = parse(sys.argv[1])
    dump_ast(ast)

    p = past.parse("""
def f(x, y):
    z = x + y
    print(z)

f(2, 3)
""")

    print(past.dump(p, indent=2))
    print(past.unparse(p))

    h2py_ast = h2py(ast)
    print(past.dump(h2py_ast, indent=2))
    print(past.unparse(h2py_ast))
