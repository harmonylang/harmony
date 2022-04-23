from functools import cmp_to_key
import inspect
from typing import Dict, Union
import random


class H2PyRuntimeException(Exception):
    pass


class HValue:

    def __eq__(self, other):
        if isinstance(other, HType):
            return hcompare(self, other) == 0
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, HType):
            return hcompare(self, other) < 0
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, HType):
            return hcompare(self, other) > 0
        else:
            return False


class HAddr(HValue):

    def __init__(self, *args):
        assert len(args) >= 1

        def flatten(arg):
            if isinstance(arg, str):
                return (arg,)
            elif isinstance(arg, HAddr):
                return arg.addr
            elif isinstance(arg, (list, tuple)):
                flattened = []
                for arg_comp in arg:
                    flattened += flatten(arg_comp)
                return tuple(flattened)

        self.addr = flatten(args)

    def __getitem__(self, item):
        return self.addr.__getitem__(item)

    def __iter__(self):
        return self.addr.__iter__()

    def __len__(self):
        return self.addr.__len__()

    def get(self):
        caller_globals = inspect.stack()[1][0].f_globals
        v = caller_globals.get(self.addr[0])
        if v is None:
            print(self.addr, caller_globals.keys())
            exit()

        for ref in self.addr[1:]:
            assert isinstance(v, HDict)
            v = v[ref]

        return v

    def assign(self, value):
        caller_globals = inspect.stack()[1][0].f_globals

        if len(self.addr) == 1:
            caller_globals[self.addr[0]] = value
        else:
            v = caller_globals[self.addr[0]]

            for ref in self.addr[1:-1]:
                assert isinstance(v, HDict)
                v = v[ref]

            assert isinstance(v, HDict)
            v[self.addr[-1]] = value


class HDict(HValue):

    def __init__(self, dict: Dict):
        self.dict = dict

    def __contains__(self, item):
        return self.dict.__contains__(item)

    def __getitem__(self, item):
        return self.dict.__getitem__(item)

    def __setitem__(self, key, value):
        return self.dict.__setitem__(key, value)

    def __iter__(self):
        return self.dict.__iter__()

    def __len__(self):
        return self.dict.__len__()

    def __call__(self, item):
        return self.dict.__getitem__(item)

    def __hash__(self):
        return hash(self.items())

    def items(self):
        return tuple(sorted(
            self.dict.items(),
            key=cmp_to_key(lambda lhs, rhs: hcompare(lhs[0], rhs[0]))
        ))


HType = (type(None), int, bool, str, HDict, HAddr)
PType = (type(None), int, bool, str, dict)


def htypeindex(hvalue: HType):
    if isinstance(hvalue, bool):
        return 0
    elif isinstance(hvalue, int):
        return 1
    elif isinstance(hvalue, str):
        return 2
    elif isinstance(hvalue, HDict):
        return 4
    elif isinstance(hvalue, (type(None), HAddr)):
        return 6
    else:
        raise NotImplementedError(hvalue)


def hcompare_bool(lhs: bool, rhs: bool):
    if lhs == rhs:
        return 0
    else:
        return -1 if lhs == False else 1


def hcompare_int(lhs: int, rhs: int):
    if lhs == rhs:
        return 0
    else:
        return -1 if lhs < rhs else 1


def hcompare_atom(lhs: str, rhs: str):
    if lhs == rhs:
        return 0
    else:
        return -1 if lhs < rhs else 1


def hcompare_dict(lhs: HDict, rhs: HDict):
    if lhs.dict == rhs.dict:
        return 0
    else:
        return -1 if lhs.items() < rhs.items() else 1


def hcompare_addr(lhs: Union[HAddr, None], rhs: Union[HAddr, None]):
    if lhs is None:
        if rhs is None:
            return 0
        else:
            return -1
    else:
        if rhs is None:
            return 1
        elif lhs.addr == rhs.addr:
            return 0
        else:
            return -1 if lhs.addr < rhs.addr else 1


def hcompare(lhs: HType, rhs: HType):
    typeindex = htypeindex(lhs)
    if typeindex != htypeindex(rhs):
        if typeindex < htypeindex(rhs):
            return -1
        elif typeindex > htypeindex(rhs):
            return 1

    if typeindex == 0:
        return hcompare_bool(lhs, rhs)
    elif typeindex == 1:
        return hcompare_int(lhs, rhs)
    elif typeindex == 2:
        return hcompare_atom(lhs, rhs)
    elif typeindex == 4:
        return hcompare_dict(lhs, rhs)
    elif typeindex == 6:
        return hcompare_addr(lhs, rhs)
    else:
        raise NotImplementedError(lhs, rhs)


def H(obj):
    """Converts a value to its Harmony representation."""

    if obj is None:
        return None
    elif isinstance(obj, bool):
        return obj
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, dict):
        return HDict({H(k): H(v) for k, v in obj.items()})
    elif isinstance(obj, HDict):
        return HDict(obj.dict)
    elif isinstance(obj, HAddr):
        return obj
    else:
        raise NotImplementedError(obj)


def P(obj):
    """Converts a value to its Python representation."""

    if obj is None:
        return None
    elif isinstance(obj, bool):
        return obj
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, str):
        return obj
    elif isinstance(obj, dict):
        return {P(k): P(v) for k, v in obj.items()}
    elif isinstance(obj, HDict):
        return {P(k): P(v) for k, v in obj.items()}
    elif isinstance(obj, HAddr):
        raise H2PyRuntimeException(
            f'Harmony object {obj} of type HAddr has no corresponding Python representation.')
    else:
        raise NotImplementedError(obj)


def choose(obj):
    if isinstance(obj, HDict):
        return random.choice(list(obj.dict.values()))
    else:
        raise NotImplementedError(obj)
