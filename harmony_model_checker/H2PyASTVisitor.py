from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor

import harmony_model_checker.harmony.ast as hast  # hast = Harmony AST
import ast as past  # past = Python AST


# Symbolic constants for indexing into a token.
T_TOKEN = 0
T_FILE = 1
T_LINENO = 2
T_COLNO = 3


class H2PyEnv:

    def __init__(self):
        self._parent = None
        self._ctx = None

    def rep(self, **kwargs):
        child = H2PyEnv()
        child._parent = self
        child._ctx = kwargs.get('ctx')
        return child

    def ctx(self):
        env = self
        while env is not None:
            if env._ctx is not None:
                return env._ctx
            env = env._parent
        return None


class H2PyASTVisitor(AbstractASTVisitor):

    def __call__(self, node: hast.AST, env: H2PyEnv = H2PyEnv()) -> past.AST:
        return node.accept_visitor(self, env)

    def visit_block(self, node: hast.BlockAST, env: H2PyEnv):
        return past.Module(
            body=[self(child, env) for child in node.b],
            type_ignores=[]
        )

    def visit_location(self, node: hast.LocationAST, env: H2PyEnv):
        return self(node.ast, env)

    # TODO: handle hast.AssignmentAST.op
    def visit_assignment(self, node: hast.AssignmentAST, env: H2PyEnv):
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
            value=self(node.rv, env.rep(ctx=past.Load())),
            lineno=node.token[T_LINENO]
        )

    def visit_name(self, node: hast.NameAST, env: H2PyEnv):
        return past.Name(id=node.name[T_TOKEN], ctx=env.ctx())

    def visit_nary(self, node: hast.NaryAST, env: H2PyEnv):
        op = node.op[T_TOKEN]
        if op == '+':
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Add(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == "*":
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Mult(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        elif op == "-":
            return past.BinOp(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                op=past.Sub(),
                right=self(node.args[1], env.rep(ctx=past.Load()))
            )

        else:
            raise NotImplementedError(op)

    def visit_constant(self, node: hast.ConstantAST, env: H2PyEnv):
        return past.Constant(value=node.const[T_TOKEN])

    def visit_print(self, node: hast.PrintAST, env: H2PyEnv):
        return past.Expr(
            value=past.Call(
                func=past.Name(id='print', ctx=past.Load()),
                args=[self(node.expr, env.rep(ctx=past.Load()))],
                keywords=[]
            )
        )

    # TODO: Smartly add function prologue and epilogue
    def visit_method(self, node: hast.MethodAST, env: H2PyEnv):
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
                self(node.stat, env),
                past.Return(
                    value=past.Name(id="result", ctx=past.Load())
                )
            ],
            decorator_list=[],
            lineno=node.token[T_LINENO]
        )

    def visit_call(self, node: hast.CallAST, env: H2PyEnv):
        return self(node.expr, env)

    # TODO: what if apply is on a dictionary?
    def visit_apply(self, node: hast.ApplyAST, env: H2PyEnv):
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

    def visit_tuple(self, node: hast.TupleAST, env: H2PyEnv):
        return past.Tuple(
            elts=[self(subnode, env) for subnode in node.list],
            ctx=env.ctx()
        )

    def visit_assert(self, node: hast.AssertAST, env: H2PyEnv):
        return past.Assert(
            test=self(node.cond, env)
        )

    def visit_cmp(self, node: hast.CmpAST, env: H2PyEnv):
        assert len(node.ops) == 1

        op = node.ops[0][T_TOKEN]
        if op == "==":
            return past.Compare(
                left=self(node.args[0], env.rep(ctx=past.Load())),
                ops=[past.Eq()],
                comparators=[self(node.args[1], env.rep(ctx=past.Load()))]
            )

        else:
            raise NotImplementedError()

    def visit_let(self, node: hast.LetAST, env: H2PyEnv):
        stmts = []
        for var, expr in node.vars:
            stmts.append(past.Assign(
                targets=[past.Name(id=var[T_TOKEN], ctx=past.Store())],
                value=self(expr, env.rep(ctx=past.Load())),
                lineno=node.token[T_LINENO]
            ))

        stmts.append(self(node.stat, env))

        for var, _ in node.vars:
            stmts.append(past.Assign(
                targets=[past.Name(id=var[T_TOKEN], ctx=past.Store())],
                value=past.Constant(value=None),
                lineno=node.token[T_LINENO]
            ))

        return stmts

    def visit_dict(self, node: hast.DictAST, env: H2PyEnv):
        return past.Call(
            func=past.Attribute(
                value=past.Name(id='h2py_runtime', ctx=past.Load()),
                attr='HDict',
                ctx=past.Load()
            ),
            args=[
                past.Dict(
                    keys=[self(key, env) for key, _ in node.record],
                    values=[self(value, env) for _, value in node.record]
                )
            ],
            keywords=[]
        )
