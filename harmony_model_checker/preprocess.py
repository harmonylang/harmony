#!/usr/bin/env python3
"""Combined test harness for harmony_parser.py and checker.py: parse a
Harmony source file and run the identifier checker over it, reporting
every syntax error, identifier error, and identifier warning found,
each with a precise, human-readable location.

Usage:
    python3 harmony_model_checker/preprocess.py path/to/program.hny [module=path/to/module.hny ...]
(or, run as a module: python3 -m harmony_model_checker.preprocess ...)

A syntax error stops there (nothing downstream of a parse failure is
checkable). Otherwise both the whole-program global-namespace check
(Phase 1: import/const/def/builtin uniqueness) and the per-function
local-namespace + '?'/assignment-target checks (Phase 2) run over the
successfully-parsed program. `from module import ...` (explicit names
or '*') is resolved against that module's own source, found by trying,
in order: an explicit `module=path` entry (feeding checker.py's
`module_map`), `<module>.hny` next to the file being checked, then
`<module>.hny` in checker.py's DEFAULT_MODULE_DIR (Harmony's own
bundled modules) - so ordinary standard-library imports like `synch`
resolve with no `module=` argument needed at all.

This is a standalone development tool (run it directly against any
.hny file to see what the checker makes of it) - main.py's own Phase 0
precheck is the integrated version of the same idea, wired into the
real compiler pipeline; see handle_precheck there.
"""

import sys

# checker.py/harmony_parser.py are this module's own siblings, inside
# the harmony_model_checker package - a relative import is all that's
# normally needed. The fallback covers running this file directly by
# path from within that same directory (python3 preprocess.py ...),
# where there's no enclosing package for a relative import to resolve
# against, but checker.py/harmony_parser.py are still right there as
# plain sibling files.
try:
    from . import checker as C
    from . import harmony_parser as P
except ImportError:
    import checker as C
    import harmony_parser as P


def offset_to_line_col(document, offset):
    """1-based line and column for a character offset."""
    line = document.count('\n', 0, offset) + 1
    line_start = document.rfind('\n', 0, offset) + 1
    col = offset - line_start + 1
    return line, col


def show_context(document, offset, width=60):
    """The source line containing offset, with a caret under it."""
    line_start = document.rfind('\n', 0, offset) + 1
    line_end = document.find('\n', offset)
    if line_end == -1:
        line_end = len(document)
    text = document[line_start:line_end]
    col = offset - line_start
    # keep long lines readable by centering the window on the error
    start = max(0, col - width // 2)
    end = min(len(text), start + width)
    snippet = text[start:end]
    caret = ' ' * (col - start) + '^'
    return snippet, caret


def _report(path, document, offset, level, message):
    line, col = offset_to_line_col(document, offset)
    snippet, caret = show_context(document, offset)
    print("%s:%d:%d: %s: %s" % (path, line, col, level, message))
    print("    " + snippet)
    print("    " + caret)


def main(argv):
    if len(argv) < 2:
        print("usage: python3 preprocess.py path/to/program.hny [module=path.hny ...]",
              file=sys.stderr)
        return 2

    path = argv[1]
    module_map = {}
    for arg in argv[2:]:
        name, _, mod_path = arg.partition('=')
        module_map[name] = mod_path

    try:
        with open(path, 'r') as f:
            document = f.read()
    except OSError as e:
        print("error: could not read %s: %s" % (path, e.strerror or e), file=sys.stderr)
        return 2

    result = P.parse_program(document)

    if not (result.success and result.end == len(document)):
        if result.success:
            # parse_program returned success but stopped short of EOF -
            # point at wherever it left off, since that's where things
            # went wrong.
            offset = result.end
            message = "parser stopped before end of file"
        else:
            offset = result.start
            message = str(result.value)
        _report(path, document, offset, "error", message)
        return 1

    # Syntax is clean - now run the identifier checker (Phases 1 and 2).
    program = C.check_identifiers(document, module_map, source_label=path)
    for err in program.errors:
        _report(path, document, err.start, "error", err.message)
    for warn in program.warnings:
        _report(path, document, warn.start, "warning", warn.message)

    if program.errors:
        return 1
    print("OK: %s parsed cleanly and has no identifier problems (%d statement(s))"
          % (path, len(result.value)))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
