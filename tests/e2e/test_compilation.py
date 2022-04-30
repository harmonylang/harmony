
from datetime import timedelta
import pathlib
from typing import List, NamedTuple
import unittest

from harmony_model_checker.compile import do_compile

class Test(NamedTuple):
    filename: pathlib.Path
    max_time: timedelta

def load_harmony_files() -> List[Test]:
    code_dir = pathlib.Path(__file__).parent.parent.parent / "code"
    return [
        Test(
            filename=f,
            max_time=timedelta(seconds=1)
        ) for f in code_dir.glob("*.hny")
    ]

class TestCompilation(unittest.TestCase):
    def test_compilation(self):
        for h in load_harmony_files():
            with self.subTest(msg=f"Checking {str(h.filename)}"):
                do_compile(str(h.filename), consts=[], mods=[], interface=None)

if __name__ == "__main__":
    unittest.main()
