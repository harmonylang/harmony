
from io import TextIOWrapper
import json
from harmony_model_checker.harmony.ast import getImported
from harmony_model_checker.harmony.code import Code
from harmony_model_checker.harmony.scope import Scope

from json_stream.writer import streamable_dict, streamable_list # type: ignore


@streamable_dict
def _dump_identifiers(scope: Scope):
    for k, (t, _) in scope.pmap.items():
        yield k, t
    yield "___", "___"


@streamable_dict
def _dump_module(scope: Scope):
    yield 'file', scope.file
    with open(scope.file, encoding='utf-8') as fdx:
        lines = fdx.read().splitlines()
    yield 'lines', streamable_list(lines)
    yield 'identifiers', _dump_identifiers(scope)


@streamable_dict
def _dump_labels(code: Code, scope: Scope):
    for k, v in scope.labels.items():
        yield str(k), str(v)
    yield "__end__", len(code.labeled_ops)


@streamable_dict
def _dump_modules(scope: Scope):
    imported = getImported()
    for module_name, mod_scope in imported.items():
        yield module_name, _dump_module(mod_scope)
    yield "__main__", _dump_module(scope)


@streamable_list
def _dump_locs(code: Code):
    for lop in code.labeled_ops:
        (_, file, line, column) = lop.start
        (endlexeme, _, endline, endcolumn) = lop.stop
        endcolumn += len(endlexeme) - 1
        if lop.stmt is None:
            line1 = line
            column1 = column
            line2 = endline
            column2 = endcolumn
        else:
            (line1, column1, line2, column2) = lop.stmt
        if (line, column) < (line1, column1):
            line = line1
            column = column1
        if (line, column) > (line2, column2):
            line = line2
            column = column2
        if (endline, endcolumn) > (line2, column2):
            endline = line2
            endcolumn = column2
        if (endline, endcolumn) < (line1, column1):
            endline = line1
            endcolumn = column1
        assert line <= endline
        assert (line < endline) or (column <= endcolumn), (lop.module, line, endline, column, endcolumn, lop.start, lop.stop, lop.stmt)
        if file is not None:
            if endlexeme in { "indent", "dedent" }:
                endlexeme = endlexeme[0]
            if lop.module is None:
                module = "__None__"
            else:
                module = lop.module
            yield {
                'module': module,
                'line': line,
                'column': column,
                'endline': endline,
                'endcolumn': endcolumn,
                'stmt': [line1, column1, line2, column2]
            }


@streamable_dict
def _dump_hvm(code: Code, scope: Scope):
    yield 'labels', _dump_labels(code, scope)
    yield 'modules', _dump_modules(scope)
    yield 'code', streamable_list(l_op.op.as_json() for l_op in code.labeled_ops)
    yield 'pretty', streamable_list([str(l_op.op), l_op.op.explain()] for l_op in code.labeled_ops)
    yield 'locs', _dump_locs(code)


def dump_json_code(code: Code, scope: Scope, f: TextIOWrapper):
    json.dump(_dump_hvm(code, scope), f, indent=2)
