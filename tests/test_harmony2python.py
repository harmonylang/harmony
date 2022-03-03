import unittest

from harmony_model_checker.harmony.DumpASTVisitor import DumpASTVisitor
from harmony_model_checker.H2PyASTVisitor import H2PyASTVisitor
from harmony_model_checker.compile import parse_string
import ast as past


class TestHarmony2Python(unittest.TestCase):

    def assert_h2py(self, harmony_code: str, python_code: str):
        h2py = H2PyASTVisitor()
        dump_ast = DumpASTVisitor()
        harmony_ast = parse_string(harmony_code)

        try:
            python_ast = h2py(harmony_ast)

        except Exception as error:
            self.fail(f"""
Error while calling H2PyASTVisitor: {error}

Dump Harmony AST: {dump_ast(harmony_ast)}
""")

        try:
            unparsed = past.unparse(python_ast)

        except Exception as error:
            self.fail(f"""
Error while unparsing Python AST: {error}

Dump Harmony AST: {dump_ast(harmony_ast)}

Dumped Parsed Python AST: {past.dump(python_ast, indent=2)}

Expected Python AST: {past.dump(past.parse(python_code), indent=2)}
""")

        self.assertEqual(python_code.strip(), unparsed.strip())

    def test_1(self):
        self.assert_h2py((
            "print(5)\n"
        ), (
            "print(5)\n"
        ))

    def test_2(self):
        self.assert_h2py((
            "def f(x):\n"
            "    print(x)\n"
            "f(5)\n"
        ), (
            "def f(x):\n"
            "    print(x)\n"
            "f(5)\n"
        ))

    def test_3(self):
        self.assert_h2py((
            "x, y = 3, 4\n"
            "print(x + y)\n"
        ), (
            "(x, y) = (3, 4)\n"
            "print(x + y)\n"
        ))


if __name__ == '__main__':
    unittest.main()
