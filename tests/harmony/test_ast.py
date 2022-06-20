from unittest import TestCase
import unittest

from harmony_model_checker.harmony.ast import *
from harmony_model_checker.harmony.code import Labeled_Op

def create_token(value, file='test.hny', line=0, col=0):
    return value, file, line, col

class TestConstantAST(TestCase):
    def create_constant_ast(self):
        return [
            ConstantAST(
                endtoken=create_token(const),
                const=create_token(const),
            ) for const in [12, True, "str"]
        ]

    def test_is_constant(self):
        for c in self.create_constant_ast():
            scope = Scope(None)
            self.assertTrue(c.isConstant(scope))

    def test_compile(self):
        for c in self.create_constant_ast():
            scope = Scope(None)
            code = Code()
            c.compile(scope, code)
            self.assertEqual(len(code.labeled_ops), 1)

            lbled_op: Labeled_Op = code.labeled_ops[0]
            self.assertIsInstance(lbled_op, Labeled_Op)

            op: PushOp = lbled_op.op
            self.assertIsInstance(op, PushOp)
            self.assertEqual(op.constant, c.const)


class TestNameAST(TestCase):
    def create_name_ast(self):
        return [
            NameAST(
                endtoken=create_token(name),
                name=create_token(name),
            ) for name in ['abc', 'foo', 'bar', 'harmony']
        ]
    
    def test_is_constant(self):
        for n in self.create_name_ast():
            # default scope is global
            scope = Scope(None)
            self.assertFalse(n.isConstant(scope))

            scope = Scope(None)
            lexeme = n.name[0]
            scope.names[lexeme] = ("constant", n.name)
            self.assertTrue(n.isConstant(scope))
    
    def test_compile(self):
        for n in self.create_name_ast():
            lexeme = n.name[0]

            # test with global scope
            scope = Scope(None)
            code = Code()
            n.compile(scope, code)
            self.assertEqual(len(code.labeled_ops), 1)
            lbled_op: Labeled_Op = code.labeled_ops[0]
            self.assertIsInstance(lbled_op, Labeled_Op)
            op: LoadOp = lbled_op.op
            self.assertIsInstance(op, LoadOp)
            self.assertEqual(op.name, n.name)

            # test as a local variable
            scope = Scope(None)
            scope.names[lexeme] = ("local-var", n.name)
            code = Code()
            n.compile(scope, code)
            self.assertEqual(len(code.labeled_ops), 1)
            lbled_op: Labeled_Op = code.labeled_ops[0]
            self.assertIsInstance(lbled_op, Labeled_Op)            
            op: LoadVarOp = lbled_op.op
            self.assertIsInstance(op, LoadVarOp)
            self.assertEqual(op.v, n.name)

            # test as a constant
            scope = Scope(None)
            scope.names[lexeme] = ("constant", n.name)
            code = Code()
            n.compile(scope, code)
            self.assertEqual(len(code.labeled_ops), 1)
            lbled_op: Labeled_Op = code.labeled_ops[0]
            self.assertIsInstance(lbled_op, Labeled_Op)
            op: PushOp = lbled_op.op
            self.assertIsInstance(op, PushOp)
            self.assertEqual(op.constant, n.name)


class TestHarmonyAST(TestCase):
    """Tests the creation and modification of Harmony AST classes
    """
    def test_create(self):
        pass

    def test_simple(self):
        self.assertTrue(True)
        pass


if __name__ == "__main__":
    unittest.main()
