from load_test_files import *

import time
import pytest
from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection

import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.compile import do_compile

@pytest.fixture(autouse=True)
def run_around_tests():
    legacy_harmony.files.clear()           # files that have been read already
    legacy_harmony.modules.clear()         # modules modified with -m
    legacy_harmony.used_modules.clear()    # modules modified and used
    legacy_harmony.namestack.clear()       # stack of module names being compiled

    legacy_harmony.imported.clear()
    legacy_harmony.constants.clear()
    legacy_harmony.used_constants.clear()
    yield

@pytest.mark.parametrize("param", load_public_harmony_files()
                                + load_constant_defined_harmony_files()
                                + load_module_defined_harmony_files())
def test_compilation_success(param):
    start_time = time.perf_counter_ns()
    do_compile(str(param.filename), consts=param.constants, mods=param.modules, interface=None)
    end_time = time.perf_counter_ns()
    duration = end_time - start_time
    assert duration <= param.max_time.total_seconds() * 1e9

@pytest.mark.parametrize("param", load_failing_harmony_files()
                                + load_failing_constant_defined_harmony_files()
                                + load_failing_module_defined_harmony_files())
def test_compilation_error(param):
    start_time = time.perf_counter_ns()
    with pytest.raises((HarmonyCompilerErrorCollection, HarmonyCompilerError)):
        do_compile(str(param.filename), consts=param.constants, mods=param.modules, interface=None)
    end_time = time.perf_counter_ns()
    duration = end_time - start_time
    assert duration <= param.max_time.total_seconds() * 1e9
