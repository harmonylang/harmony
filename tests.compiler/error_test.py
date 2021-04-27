import os
import pathlib
import stat
import subprocess
import importlib.util
import sys
import inspect
import tempfile
from abc import abstractmethod
from typing import Any, List, Callable

PROJECT_DIR = pathlib.Path(__file__).resolve().parent.parent


class TestInstance:
    @abstractmethod
    def content(self) -> List[str]:
        pass
    @abstractmethod
    def validate(self) -> Callable[[Any], bool]:
        pass
class AddressFromValue(TestInstance):
    def content(self) -> List[str]:
        return ["const C=3\ns=?C",
                "g=?2",
                "g=?False",
                "let f = 4:\n    g=?f",
                "import synch\ng=?synch"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'TakeAddressError'
class CatchAssignmentErrors(TestInstance):
    def content(self) -> List[str]:
        return ["const C=3\nC=10",
                "const G=32\nG+=1",
                "import bag\nbag=3",
                "import bag\nbag+=method()"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'AssignmentError'
class CatchImportError(TestInstance):
    def content(self) -> List[str]:
        return [
            "from synch import unknown_value",
            "from unknown_module import whatever",
            "import unknown_module"
        ]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'ImportError'
class CatchInvalidConstantError(TestInstance):
    def content(self) -> List[str]:
        return [
            "const C = function_results_are_not_constant()",
            "const C = 1 + a()",
            "const C = variables_are_not_constants",
            "import synch\nconst C = synch"
        ]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'InvalidConstantError'
class CatchUnexpectedEofError(TestInstance):
    def content(self) -> List[str]:
        return ["",
                "if True",
                "while True:\n",
                "if True:\n",
                "let k = 23:\n"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'UnexpectedEofError'
class CatchEmptyStatementError(TestInstance):
    def content(self) -> List[str]:
        return ["def function():\n    \nk = 32"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'EmptyStatementError'
class CatchMissingExpressionError(TestInstance):
    def content(self) -> List[str]:
        return ["e = 34 + const",
                "const g = 13 < ^",
                'd = 3 if True else &',
                "c = v if * else 23"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == "MissingExpressionError"
class CatchEmptyStatementError(TestInstance):
    def content(self) -> List[str]:
        return ["f = 2 + ", "const g = 3 + "]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'IncompleteStatementError'
class CatchMissingBracketError(TestInstance):
    def content(self) -> List[str]:
        return ["(",
                "g = (25 + 4",
                "{3,5,6",
                "['a'"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'MissingBracketError'
class CatchUnmatchedBracketError(TestInstance):
    def content(self) -> List[str]:
        return ["(3,5},6",
                "{'a']"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'UnmatchedBracketError'
class CatchUnexpectedTokenError(TestInstance):
    def content(self) -> List[str]:
        return ["spawn not_a_function",
                "trap a", "go mod",
                "sequential cs4110-",
                "del *", "spawn ^",
                "trap @", "go @",
                "sequential @",
                "import this now",
                "from here import this now",
                "assert *, *", "assert *"]
    def validate(self) -> Callable[[Any], bool]:
        return lambda e: e.error_name == 'UnexpectedTokenError'


def collect_classes():
    classes = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, TestInstance) and obj is not TestInstance:
            classes.append(obj)
    return classes


def assert_raises(file_content, validate, main):
    for content in file_content:
        fd, path = tempfile.mkstemp(prefix="harmony-compiler-test")
        pathlib.Path(path).chmod(pathlib.Path(path).stat().st_mode | stat.S_IREAD | stat.S_IWRITE)
        with open(path, 'w') as f:
            f.write(content)
        os.close(fd)

        try:
            main(['python', '-A', path])
            assert False, 'Failed to catch compiler error correctly'
        except Exception as e:
            print(e)
            assert validate(e), f'Validation failed, Error: {e},\nContent:\n{content}'
        finally:
            os.unlink(path)


def cleanup_files():
    (PROJECT_DIR / "harmony.py").unlink()
    (PROJECT_DIR / "src" / "harmony" / "buildversion").unlink()


def test_runner():
    subprocess.run(['make', 'all'], cwd=str(PROJECT_DIR), stdout=open(os.devnull))

    spec: Any = importlib.util.spec_from_file_location('.', str(PROJECT_DIR / 'harmony.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, 'main'):
        raise ValueError("Cannot find main in harmony.py module")
    main = module.__getattribute__('main')
    test_classes = collect_classes()
    for t in test_classes:
        instance = t()
        content, validate = instance.content(), instance.validate()
        try:
            assert_raises(content, validate, main)
        except Exception as e:
            print(f"Failed to validate instance {instance.__class__.__name__}, {e}")
            return
    print('All given tests pass! ✅ ')
    print(f'Tested {len(test_classes)} error test instances')


if __name__ == "__main__":
    test_runner()
    cleanup_files()
