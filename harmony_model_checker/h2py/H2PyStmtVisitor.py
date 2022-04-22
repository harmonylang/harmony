from typing import Tuple
from harmony_model_checker.h2py.H2PyEnv import H2PyEnv
from harmony_model_checker.h2py.H2PyExprVisitor import H2PyExprVisitor
from harmony_model_checker.h2py.util import *
from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor
import harmony_model_checker.harmony.ast as hast

import ast as past


class H2PyStmtVisitor(AbstractASTVisitor):


    def __call__(self, node: hast.AST, env: H2PyEnv = H2PyEnv()) -> past.AST:
        return node.accept_visitor(self, env)

    def visit_block(self, node: hast.BlockAST, env: H2PyEnv):
        return [self(child, env) for child in node.b]

    def visit_location(self, node: hast.LocationAST, env: H2PyEnv):
        return self(node.ast, env)

    def visit_assignment(self, node: hast.AssignmentAST, env: H2PyEnv):
        h2expr = H2PyExprVisitor()

        supported = {'='}
        if (node.op[T_TOKEN] not in supported):
            raise NotImplementedError(
                f'{node.op[T_TOKEN]} is not a supported assignment operator. '
                f'Supported assignment operators are currently {supported}'
            )

        def convert_target(target):
            if isinstance(target, list):
                return [convert_target(target) for target in target]

            elif isinstance(target, hast.TupleAST):
                return past.Tuple(
                    elts=[convert_target(target) for target in target.list],
                    ctx=past.Store()
                )

            elif isinstance(target, hast.NameAST):
                return past.Name(
                    id=escape_name(target.name[T_TOKEN]), 
                    ctx=past.Store()
                )

            elif isinstance(target, hast.ApplyAST):
                return past.Subscript(
                    value=h2expr(target.method, env),
                    slice=h2expr(target.arg, env),
                    ctx=past.Store()
                )

            elif isinstance(target, hast.AddressAST):
                return h2expr(target)

            elif isinstance(target, hast.PointerAST):
                assert False, 'Pointer assignment is only supported in single-assignment form.'

            else:
                assert False, f'Unable to convert target {target}'

        if len(node.lhslist) == 1 and isinstance(node.lhslist[0], hast.PointerAST):
            return past.Expr(
                value=past.Call(
                    func=past.Attribute(
                        value=h2expr(node.lhslist[0].expr, env.rep(ctx=past.Load())),
                        attr='assign'
                    ),
                    args=[h2expr(node.rv, env.rep(ctx=past.Load()))],
                    keywords=[]
                )
            )

        value = h2expr(node.rv, env.rep(ctx=past.Load()))

        return past.Assign(
            targets=convert_target(node.lhslist),
            value=value,
            lineno=node.token[T_LINENO]
        )

    def visit_print(self, node: hast.PrintAST, env: H2PyEnv):
        h2expr = H2PyExprVisitor()
        args = [h2expr(node.expr, env.rep(ctx=past.Load()))]

        return past.Expr(
            value=past.Call(
                func=past.Name(id='print', ctx=past.Load()),
                args=args,
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
                    targets=[past.Name(id='result', ctx=past.Store())],
                    value=past.Constant(value=None),
                    lineno=node.token[T_LINENO]
                ),
                *self(node.stat, env),
                past.Return(
                    value=past.Name(id='result', ctx=past.Load())
                )
            ],
            decorator_list=[],
            lineno=node.token[T_LINENO]
        )

    def visit_call(self, node: hast.CallAST, env: H2PyEnv):
        h2expr = H2PyExprVisitor()
        return [past.Expr(value=h2expr(node.expr))]

    def visit_assert(self, node: hast.AssertAST, env: H2PyEnv):
        h2expr = H2PyExprVisitor()
        return past.Assert(
            test=h2expr(node.cond, env)
        )

    def visit_let(self, node: hast.LetAST, env: H2PyEnv):
        stmts = []
        for var, expr in node.vars:
            h2expr = H2PyExprVisitor()
            value = h2expr(expr, env.rep(ctx=past.Load()))
            stmts.append(past.Assign(
                targets=[past.Name(id=var[T_TOKEN], ctx=past.Store())],
                value=value,
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

    def visit_from(self, node: hast.FromAST, env: H2PyEnv):
        if node.items:
            names = [past.alias(name=name[T_TOKEN]) for name in node.items]
        else:
            names = [past.alias(name='*')]

        return past.ImportFrom(
            module=node.module[T_TOKEN],
            names=names,
            level=0
        )

    def visit_import(self, node: hast.ImportAST, env: H2PyEnv):
        return past.Import(
            names=[past.alias(name=name[T_TOKEN]) for name in node.modlist]
        )

    def visit_if(self, node: hast.IfAST, env: H2PyEnv):
        h2expr = H2PyExprVisitor()

        def compile_alts(alts: list[Tuple[hast.AST, hast.AST, any, any]], else_stmt: hast.AST):
            if len(alts) == 0:
                if else_stmt is not None:
                    return self(else_stmt, env)
                else:
                    return []
            
            (cond, stmt, _1, _2) = alts[0]
            return [past.If(
                test=h2expr(cond, env),
                body=self(stmt, env),
                orelse=compile_alts(alts[1:], else_stmt)
            )]
        
        return compile_alts(node.alts, node.stat)

    def visit_var(self, node: hast.VarAST, env: H2PyEnv):
        stmts = []

        def convert_target(var):
            if isinstance(var, list):
                return past.Tuple(elts=[convert_target(var) for var in var])
            elif isinstance(var, tuple):
                return past.Name(id=var[T_TOKEN])
            else:
                assert False, f'Unable to convert target {var}'

        for var, expr in node.vars:
            h2expr = H2PyExprVisitor()
            value = h2expr(expr, env.rep(ctx=past.Load()))
            stmts.append(past.Assign(
                targets=[convert_target(var)],
                value=value,
                lineno=node.token[T_LINENO]
            ))

        return stmts

    def visit_while(self, node: hast.WhileAST, env: H2PyEnv):
        h2expr = H2PyExprVisitor()

        return past.While(
            test=h2expr(node.cond, env),
            body=self(node.stat, env), 
            orelse=[]
        )
