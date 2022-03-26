from harmony_model_checker.h2py.H2PyEnv import H2PyEnv
from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor
from harmony_model_checker.h2py.token import *
import harmony_model_checker.h2py.h2py_runtime as h2py_runtime
import harmony_model_checker.harmony.ast as hast

import ast as past


class H2PyExprVisitor(AbstractASTVisitor):

    def __init__(self):
        self.prologue = []
        self.epilogue = []

    def __call__(self, node: hast.AST, env: H2PyEnv = H2PyEnv()) -> past.AST:
        return node.accept_visitor(self, env)

    def visit_name(self, node: hast.NameAST, env: H2PyEnv):
        name = node.name[T_TOKEN]
        while name in dir(h2py_runtime):
            name = f'_{name}'
        return past.Name(id=name, ctx=env.get('ctx'))

    def visit_nary(self, node: hast.NaryAST, env: H2PyEnv):
        op = node.op[T_TOKEN]

        if op == '+':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Add(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == '*':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Mult(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == '-':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Sub(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == 'and':
            return past.BoolOp(
                op=past.And(),
                values=[
                    self(node.args[0], env.rep(ctx=past.Load())),
                    self(node.args[1], env.rep(ctx=past.Load()))
                ]
            )

        elif op == 'or':
            return past.BoolOp(
                op=past.Or(),
                values=[
                    self(node.args[0], env.rep(ctx=past.Load())),
                    self(node.args[1], env.rep(ctx=past.Load()))
                ]
            )

        elif op == '=>':
            return past.BoolOp(
                op=past.Or(),
                values=[
                    past.UnaryOp(
                        op=past.Not(),
                        operand=self(node.args[0], env.rep(ctx=past.Load()))
                    ),
                    self(node.args[1], env.rep(ctx=past.Load()))
                ]
            )

        elif op == '&':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.BitAnd(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == '|':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.BitOr(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == '^':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.BitXor(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op in {'//', '/'}:
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.FloorDiv(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op in {'%', 'mod'}:
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Mod(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op in {'**'}:
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Pow(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == '<<':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.LShift(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == '>>':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.RShift(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        else:
            raise NotImplementedError(op)

    def visit_cmp(self, node: hast.CmpAST, env: H2PyEnv):
        assert(len(node.ops) == 1)

        op = node.ops[0][T_TOKEN]
        if op == '==':
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.Eq()],
                comparators=[
                    self(node.args[1], env.rep(ctx=past.Load())),
                ]
            )

        elif op == '!=':
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.NotEq()],
                comparators=[
                    self(node.args[1], env.rep(ctx=past.Load())),
                ]
            )

        elif op == '<':
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.Lt()],
                comparators=[
                    self(node.args[1], env.rep(ctx=past.Load())),
                ]
            )

        elif op == '<=':
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.LtE()],
                comparators=[
                    self(node.args[1], env.rep(ctx=past.Load())),
                ]
            )

        elif op == '>':
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.Gt()],
                comparators=[
                    self(node.args[1], env.rep(ctx=past.Load())),
                ]
            )

        elif op == '>=':
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.GtE()],
                comparators=[
                    self(node.args[1], env.rep(ctx=past.Load())),
                ]
            )

        else:
            raise NotImplementedError(op)

    def visit_constant(self, node: hast.ConstantAST, env: H2PyEnv):
        return past.Constant(value=node.const[T_TOKEN])

    def visit_tuple(self, node: hast.TupleAST, env: H2PyEnv):
        return past.Tuple(
            elts=[self(subnode, env) for subnode in node.list],
            ctx=env.get('ctx')
        )

    def visit_dict(self, node: hast.DictAST, env: H2PyEnv):
        return past.Call(
            func=past.Name(id='H', ctx=past.Load()),
            args=[
                past.Dict(
                    keys=[self(key, env) for key, _ in node.record],
                    values=[self(value, env) for _, value in node.record]
                )
            ],
            keywords=[]
        )

    def visit_apply(self, node: hast.ApplyAST, env: H2PyEnv):
        def convert_addr_lv(lv):
            if isinstance(lv, hast.NameAST):
                return (lv.name[T_TOKEN],)
            elif isinstance(lv, hast.ApplyAST) and isinstance(lv.method, hast.NameAST):
                return (lv.method.name[T_TOKEN], *convert_addr_lv(lv.arg))
            elif isinstance(lv, hast.ConstantAST):
                return (lv.const[T_TOKEN],)
            else:
                assert False, f'Unable to convert addr lv {lv}'

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

            elif isinstance(arg, hast.AddressAST):
                return [past.Call(
                    func=past.Name(id='HAddr', ctx=past.Load()),
                    args=[past.Constant(value=convert_addr_lv(arg.lv))],
                    keywords=[]
                )]

            else:
                assert False, f'Unable to convert arg {arg}'

        if isinstance(node.method, hast.NameAST):
            return past.Call(
                func=past.Name(id=node.method.name[T_TOKEN], ctx=past.Load()),
                args=convert_arg(node.arg),
                keywords=[]
            )

        else:
            raise NotImplementedError(node.method)

    def visit_pointer(self, node: hast.PointerAST, env: H2PyEnv):
        return past.Call(
            func=past.Attribute(
                value=self(node.expr, env.rep(ctx=past.Load())),
                attr='get'
            ),
            args=[],
            keywords=[]
        )
