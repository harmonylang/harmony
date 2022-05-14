import pytest
from harmony_model_checker.main import handle_hny, handle_hvm, handle_hco
import harmony_model_checker.harmony.harmony as legacy_harmony

from load_test_files import *

class MockNS:
    B = None
    noweb = True
    const = None
    mods = None
    intf = None
    module = None
    cf = []

def _replace_ext(p: pathlib.Path, ext: str):
    p_ext = p.suffix
    return str(p)[:-len(p_ext)] + '.' + ext

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
def test_gen_html(param: Params):
    mock_ns = MockNS()

    output_files = {
        "hfa": None,
        "htm": _replace_ext(param.filename, 'htm'),
        "hco": _replace_ext(param.filename, 'hco'),
        "hvm": _replace_ext(param.filename, 'hvm'),
        "png": None,
        "tla": None,
        "gv":  None
    }

    code, scope = handle_hny(mock_ns, output_files, False, str(param.filename))
    handle_hvm(mock_ns, output_files, False, code, scope)
    # handle_hco(mock_ns, output_files)
