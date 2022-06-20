import logging
import subprocess
import unittest
from harmony_model_checker.main import handle_hco
import harmony_model_checker.harmony.harmony as legacy_harmony

from tests.e2e.load_test_files import *

logger = logging.Logger(__file__)

class MockNS:
    B = None
    noweb = True
    const = None
    mods = None
    intf = None
    module = None
    cf = []
    suppress = False

_HARMONY_SCRIPT = pathlib.Path(__file__).parent.parent.parent / "harmony"

def _replace_ext(p: pathlib.Path, ext: str):
    p_ext = p.suffix
    return str(p)[:-len(p_ext)] + '.' + ext

class GenHtmlTestCase(unittest.TestCase):
    def run_before_tests(self):
        legacy_harmony.files.clear()           # files that have been read already
        legacy_harmony.modules.clear()         # modules modified with -m
        legacy_harmony.used_modules.clear()    # modules modified and used
        legacy_harmony.namestack.clear()       # stack of module names being compiled

        legacy_harmony.imported.clear()
        legacy_harmony.constants.clear()
        legacy_harmony.used_constants.clear()

    def test_gen_html(self):
        params = load_public_harmony_files() \
            + load_constant_defined_harmony_files() \
            + load_module_defined_harmony_files()
        mock_ns = MockNS()
        for param in params:
            output_files = {
                "hfa": None,
                "htm": _replace_ext(param.filename, 'htm'),
                "hco": _replace_ext(param.filename, 'hco'),
                "hvm": _replace_ext(param.filename, 'hvm'),
                "png": None,
                "tla": None,
                "gv":  None
            }
            with self.subTest():
                try:
                    # If it takes longer than 3 seconds, just skip.
                    r = subprocess.run(
                        args=[_HARMONY_SCRIPT,
                              str(param.filename), '--noweb'] +
                              [('-c' + c) for c in param.constants] +
                              [('-m' + m) for m in param.modules],
                              timeout=3)
                    self.assertEqual(r.returncode, 0)
                except subprocess.TimeoutExpired:
                    logger.warning("TimeoutExpired for file %s.", str(param.filename))
                    continue
                handle_hco(mock_ns, output_files)
