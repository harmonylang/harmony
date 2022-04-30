
from datetime import timedelta
import pathlib
from typing import List, NamedTuple
import unittest

import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.compile import do_compile

class Test(NamedTuple):
    filename: pathlib.Path
    max_time: timedelta

def load_harmony_files() -> List[Test]:
    code_dir = pathlib.Path(__file__).parent.parent.parent / "code"
    return [
        Test(
            filename=f,
            max_time=timedelta(milliseconds=500)
        ) for f in code_dir.glob("*.hny")
    ]

class TestCompilation(unittest.TestCase):
    def test_compilation(self):
        for h in load_harmony_files():
            with self.subTest(msg=f"Compiling {str(h.filename)}"):
                do_compile(str(h.filename), consts=[], mods=[], interface=None)
                legacy_harmony.files.clear()           # files that have been read already
                legacy_harmony.modules.clear()         # modules modified with -m
                legacy_harmony.used_modules.clear()    # modules modified and used
                legacy_harmony.namestack.clear()       # stack of module names being compiled

                legacy_harmony.imported.clear()
                legacy_harmony.constants.clear()
                legacy_harmony.used_constants.clear()


if __name__ == "__main__":
    unittest.main()
