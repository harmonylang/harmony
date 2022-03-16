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

        self.assertEqual(python_code.strip(), unparsed.strip(), f"""
Dump Harmony AST: {dump_ast(harmony_ast)}

Dumped Parsed Python AST: {past.dump(python_ast, indent=2)}

Expected Python AST: {past.dump(past.parse(python_code), indent=2)}
""")

    def test_1(self):
        self.assert_h2py("""
print(5)
""", """
print(5)
""")

    def test_2(self):
        self.assert_h2py("""
def f(x):
    print(x)
f(5)
""", """
def f(x):
    result = None
    print(x)
    return result
f(5)
""")

    def test_3(self):
        self.assert_h2py("""
x, y = 3, 4
print(x + y)
""", """
(x, y) = (3, 4)
print(x + y)
""")

    def test_4(self):
        self.assert_h2py("""
def f(x, y):
    let z = x + y:
        print(z)
f(3, 4)
""", """
def f(x, y):
    result = None
    z = x + y
    print(z)
    z = None
    return result
f(3, 4)
""")

    def test_5(self):
        self.assert_h2py("""
def f(x, y):
    let z = x + y:
        print(x + y)
        assert z == 5
f(2, 3)
""", """
def f(x, y):
    result = None
    z = x + y
    print(x + y)
    assert z == 5
    z = None
    return result
f(2, 3)
""")

    def test_6(self):
        self.assert_h2py("""
x = { .y: 5, .z: 10 }
print(x.y + x.z)
""", """
x = h2py_runtime.HDict({'y': 5, 'z': 10})
print(
x('y') + 
x('z'))
""")


if __name__ == '__main__':
    unittest.main()
