
from datetime import timedelta
import pathlib
import time
from typing import List, NamedTuple
import pytest

import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.compile import do_compile

class Params(NamedTuple):
    filename: pathlib.Path
    max_time: timedelta

def load_harmony_files() -> List[Params]:
    code_dir = pathlib.Path(__file__).parent.parent.parent / "code"
    return [
        Params(
            filename=f,
            max_time=timedelta(milliseconds=500)
        ) for f in code_dir.glob("*.hny")
    ]

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

@pytest.mark.parametrize("param", load_harmony_files())
def test_compilation(param):
    start_time = time.perf_counter_ns()
    do_compile(str(param.filename), consts=[], mods=[], interface=None)
    end_time = time.perf_counter_ns()
    assert end_time - start_time <= param.max_time.microseconds * 1000
