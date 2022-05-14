
from datetime import timedelta
import pathlib
import time
from typing import List, NamedTuple
import pytest
from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection

import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.compile import do_compile

class Params(NamedTuple):
    filename: pathlib.Path
    max_time: timedelta
    modules: List[str]
    constants: List[str]

def load_dir(dir: pathlib.Path, modules=None, constants=None):
    return [
        Params(
            filename=f,
            max_time=timedelta(seconds=1),
            modules=modules or [],
            constants=constants or [],
        ) for f in dir.glob("*.hny")
    ]

_DIR = pathlib.Path(__file__).parent

def load_public_harmony_files():
    code_dir = _DIR.parent.parent / "code"
    return load_dir(code_dir)

def load_failing_harmony_files():
    code_dir = _DIR / "errors"
    return load_dir(code_dir)

def load_constant_defined_harmony_files():
    code_dir = _DIR / "constants"
    return load_dir(code_dir, constants=['C=42'])

def load_failing_constant_defined_harmony_files():
    code_dir = _DIR / "constants"
    return load_dir(code_dir, constants=['C=']) \
         + load_dir(code_dir, constants=['C=42', 'A=12'])   # unused constants

def load_module_defined_harmony_files():
    code_dir = _DIR / "modules"
    return load_dir(code_dir, modules=['math=resources/math'])

def load_failing_module_defined_harmony_files():
    code_dir = _DIR / "modules"
    return load_dir(code_dir, modules=['math=resources/matt']) \
         + load_dir(code_dir, modules=['math=resources/math',
                                       'numpy=resources/numpy']) # unused modules

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
