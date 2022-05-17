import unittest
from tests.e2e.load_test_files import *

import time
from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection

import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.compile import do_compile

class CompilationTestCase(unittest.TestCase):
    def run_before_tests(self):
        legacy_harmony.files.clear()           # files that have been read already
        legacy_harmony.modules.clear()         # modules modified with -m
        legacy_harmony.used_modules.clear()    # modules modified and used
        legacy_harmony.namestack.clear()       # stack of module names being compiled

        legacy_harmony.imported.clear()
        legacy_harmony.constants.clear()
        legacy_harmony.used_constants.clear()

    def test_compilation_success(self):
        params = load_public_harmony_files() \
            + load_constant_defined_harmony_files() \
            + load_module_defined_harmony_files()
        for param in params:
            f = str(param.filename)
            self.run_before_tests()
            with self.subTest(f"Success compilation test: {f}"):
                start_time = time.perf_counter_ns()
                do_compile(f, consts=param.constants, mods=param.modules, interface=None)
                end_time = time.perf_counter_ns()
                duration = end_time - start_time
                self.assertLessEqual(duration, param.max_time.total_seconds() * 1e9)

    def test_compilation_error(self):
        params = load_failing_harmony_files() \
            + load_failing_constant_defined_harmony_files() \
            + load_failing_module_defined_harmony_files()
        for param in params:
            f = str(param.filename)
            self.run_before_tests()
            with self.subTest(f"Success compilation test: {f}"):
                start_time = time.perf_counter_ns()
                self.assertRaises(
                    (HarmonyCompilerErrorCollection, HarmonyCompilerError),
                    lambda: do_compile(f, consts=param.constants, mods=param.modules, interface=None))
                end_time = time.perf_counter_ns()
                duration = end_time - start_time
                self.assertLessEqual(duration, param.max_time.total_seconds() * 1e9)
