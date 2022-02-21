#!/usr/bin/env python3

import sys

from harmony_model_checker.compile import parse
from harmony_model_checker.harmony.AbstractASTVisitor import AbstractASTVisitor
from harmony_model_checker.harmony.DumpASTVisitor import DumpASTVisitor

import harmony_model_checker.harmony.ast as hast # hast = Harmony AST
import ast as past # past = Python AST


dump_ast = DumpASTVisitor()


class H2PyASTVisitor(AbstractASTVisitor):

    def __call__(self, node: hast.AST, **kwargs) -> past.AST:
        return node.accept_visitor(self, **kwargs)

    def visit_block(self, node: hast.BlockAST, **kwargs):
        return past.Module(
            body=[self(child, **kwargs) for child in node.b],
            type_ignores=[]
        )

    def visit_location(self, node: hast.LocationAST, **kwargs):
        return self(node.ast, **kwargs)

    def visit_assignment(self, node: hast.AssignmentAST, **kwargs):
        targets = [self(lhs, ctx=past.Store(), **kwargs) for lhs in node.lhslist]
        value = self(node.rv, ctx=past.Load(), **kwargs)
        # TODO: handle hast.AssignmentAST.op

        return past.Assign(
            targets=targets,
            value=value,
            lineno=node.token[2]
        )

    def visit_name(self, node: hast.NameAST, ctx, **kwargs):
        # TODO: What is the purpose of the ctx argument? 
        return past.Name(id=node.name[0], ctx=ctx)

    def visit_nary(self, node: hast.NaryAST, **kwargs):
        op = node.op[0]
        if op == '+':
            return past.BinOp(
                left=self(node.args[0], **kwargs),
                op=past.Add(),
                right=self(node.args[1], **kwargs)
            )
        else:
            assert False

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


h2py = H2PyASTVisitor()

def main():
    ast = parse(sys.argv[1])
    dump_ast(ast)

    p = past.parse("""
x = 2 + 3
print(x)
""")

    print(past.dump(p))
    print(past.unparse(p))

    h2py_ast = h2py(ast)
    print(past.dump(h2py_ast))
    print(past.unparse(h2py_ast))
    
