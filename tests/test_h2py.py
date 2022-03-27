import unittest

from harmony_model_checker.harmony.DumpASTVisitor import DumpASTVisitor
from harmony_model_checker.h2py.h2py import h2py
from harmony_model_checker.compile import parse_string
import ast as past


class TestH2PyProgram(unittest.TestCase):

    def assert_h2py(self, harmony_code: str, python_code: str):
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

    def assert_h2py_files(self, harmony_path: str, python_path: str):
        with open(harmony_path) as harmony_file:
            with open(python_path) as python_file:
                self.assert_h2py(harmony_file.read(), python_file.read())

    def test_print(self):
        self.assert_h2py_files(
            'tests/resources/h2py/print.hny',
            'tests/resources/h2py/print.py'
        )

    def test_func_1(self):
        self.assert_h2py_files(
            'tests/resources/h2py/func_1.hny',
            'tests/resources/h2py/func_1.py',
        )

    def test_binops(self):
        self.assert_h2py_files(
            'tests/resources/h2py/binops.hny',
            'tests/resources/h2py/binops.py',
        )

    def test_dict_assign(self):
        self.assert_h2py_files(
            'tests/resources/h2py/dict_assign.hny',
            'tests/resources/h2py/dict_assign.py',
        )

    def test_imports(self):
        self.assert_h2py_files(
            'tests/resources/h2py/imports.hny',
            'tests/resources/h2py/imports.py',
        )

    def test_local_assign_assert(self):
        self.assert_h2py_files(
            'tests/resources/h2py/local_assign_assert.hny',
            'tests/resources/h2py/local_assign_assert.py',
        )

    def test_local_assign(self):
        self.assert_h2py_files(
            'tests/resources/h2py/local_assign.hny',
            'tests/resources/h2py/local_assign.py',
        )

    def test_ptr_assign_1(self):
        self.assert_h2py_files(
            'tests/resources/h2py/ptr_assign_1.hny',
            'tests/resources/h2py/ptr_assign_1.py',
        )

    def test_ptr_assign_2(self):
        self.assert_h2py_files(
            'tests/resources/h2py/ptr_assign_2.hny',
            'tests/resources/h2py/ptr_assign_2.py',
        )

    def test_tuple_assign(self):
        self.assert_h2py_files(
            'tests/resources/h2py/tuple_assign.hny',
            'tests/resources/h2py/tuple_assign.py',
        )

    def test_h2py_name_conflict(self):
        self.assert_h2py_files(
            'tests/resources/h2py/h2py_name_conflict.hny',
            'tests/resources/h2py/h2py_name_conflict.py',
        )

    @unittest.skip('h2py_name_conflict_2.py is not semantically equivalent to h2py_name_conflict_2.hny')
    def test_h2py_name_conflict_2(self):
        self.assert_h2py_files(
            'tests/resources/h2py/h2py_name_conflict_2.hny',
            'tests/resources/h2py/h2py_name_conflict_2.py',
        )


if __name__ == '__main__':
    unittest.main()
