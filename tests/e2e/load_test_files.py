from datetime import timedelta
import pathlib
from typing import List, NamedTuple


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
