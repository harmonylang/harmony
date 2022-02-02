from typing import Dict, List, Optional
import json
import os
import pathlib
import webbrowser
import sys
import argparse

from antlr4 import *

import harmony_model_checker
import harmony_model_checker.util.self_check_is_outdated as check_version
from harmony_model_checker import charm
from harmony_model_checker.exception import HarmonyCompilerErrorCollection

import harmony_model_checker.harmony as legacy_harmony
from harmony_model_checker.harmony import tla_translate, optimize, dumpCode, run, htmldump
from harmony_model_checker.harmony import BlockAST, Code, Scope, FrameOp, ReturnOp, Brief, GenHTML, PushOp, \
    StoreOp, HarmonyCompilerError, State, ContextValue
from harmony_model_checker.parser.HarmonyParser import HarmonyParser
from harmony_model_checker.parser.HarmonyErrorListener import HarmonyLexerErrorListener, HarmonyParserErrorListener
from harmony_model_checker.parser.HarmonyLexer import HarmonyLexer
from harmony_model_checker.parser.antlr_rule_visitor import HarmonyVisitorImpl


def build_parser(progam_input: InputStream, lexer_error_listener=None, parser_error_listener=None):
    lexer = HarmonyLexer(progam_input)
    stream = CommonTokenStream(lexer)
    parser = HarmonyParser(stream)

    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    if lexer_error_listener:
        lexer.addErrorListener(lexer_error_listener)
    if parser_error_listener:
        parser.addErrorListener(parser_error_listener)

    return parser


def load_string(string, scope: Scope, code: Code, filename="<string-code>"):
    legacy_harmony.namestack.append(filename)
    ast = parse_string(string, filename)
    for mod in ast.getImports():
        do_import(scope, code, mod)
    # method names and label names get a temporary value
    # they are filled in with their actual values after compilation
    # TODO.  Look for duplicates?
    for ((lexeme, file, line, column), lb) in ast.getLabels():
        scope.names[lexeme] = ("constant", (lb, file, line, column))

    ast.compile(scope, code)
    legacy_harmony.namestack.pop()


def load_file(filename: str, scope: Scope, code: Code):
    if filename in legacy_harmony.files:
        return
    legacy_harmony.namestack.append(filename)
    with open(filename, "r") as f:
        legacy_harmony.files[filename] = f.read().split("\n")

    ast = parse(filename)
    if ast is None:
        raise HarmonyCompilerError(
            message="Unknown error: unable to parse Harmony file",
            filename=filename
        )

    for mod in ast.getImports():
        do_import(scope, code, mod)

    # method names and label names get a temporary value
    # they are filled in with their actual values after compilation
    # TODO.  Look for duplicates?
    for ((lexeme, file, line, column), lb) in ast.getLabels():
        scope.names[lexeme] = ("constant", (lb, file, line, column))

    ast.compile(scope, code)
    legacy_harmony.namestack.pop()


def do_import(scope: Scope, code: Code, module):
    (lexeme, file, line, column) = module
    # assert lexeme not in scope.names        # TODO
    if lexeme not in legacy_harmony.imported:
        # TODO.  Only do the following if the modules have variables?
        code.append(PushOp((legacy_harmony.novalue, file, line, column)))
        code.append(StoreOp(module, module, []))

        # module name replacement with -m flag
        modname = legacy_harmony.modules.get(lexeme, lexeme)

        # create a new scope
        scope2 = Scope(None)
        scope2.prefix = [lexeme]
        scope2.labels = scope.labels

        found = False
        install_path = os.path.dirname(os.path.realpath(__file__))
        for directory in [os.path.dirname(legacy_harmony.namestack[-1]), os.path.join(install_path, "modules"), "."]:
            filename = os.path.join(directory, modname + ".hny")
            if os.path.exists(filename):
                load_file(filename, scope2, code)
                found = True
                break
        if not found:
            raise HarmonyCompilerError(
                filename=file,
                lexeme=modname,
                message="Can't import module %s from %s" % (
                    modname, legacy_harmony.namestack),
                line=line,
                column=column
            )
        legacy_harmony.imported[lexeme] = scope2

    scope.names[lexeme] = ("module", legacy_harmony.imported[lexeme])


def parse_constant(name: str, value: str):
    filename = "<constant argument>"
    _input = InputStream(value)
    parser = build_parser(_input)
    visitor = HarmonyVisitorImpl(filename)

    tree = parser.expr()
    ast = visitor.visit(tree)

    scope = Scope(None)
    code = Code()
    ast.compile(scope, code)
    state = State(code, scope.labels)
    ctx = ContextValue(("__arg__", None, None, None), 0,
                       legacy_harmony.novalue, legacy_harmony.novalue)
    ctx.atomic = 1
    while ctx.pc != len(code.labeled_ops):
        code.labeled_ops[ctx.pc].op.eval(state, ctx)
    legacy_harmony.constants[name] = ctx.pop()


def parse_string(string: str, filename: str = "<string-code>") -> BlockAST:
    _input = InputStream(string)
    parser = build_parser(_input)
    visitor = HarmonyVisitorImpl(filename)

    tree = parser.program()
    return visitor.visit(tree)


def parse(filename: str) -> BlockAST:
    _input = FileStream(filename)
    error_listener = HarmonyParserErrorListener(filename)
    lexer_error_listener = HarmonyLexerErrorListener(filename)
    parser = build_parser(
        _input,
        lexer_error_listener=lexer_error_listener,
        parser_error_listener=error_listener
    )

    tree = parser.program()
    if error_listener.errors or lexer_error_listener.errors:
        raise HarmonyCompilerErrorCollection(
            lexer_error_listener.errors + error_listener.errors
        )

    visitor = HarmonyVisitorImpl(filename)
    try:
        return visitor.visit(tree)
    except HarmonyCompilerError as e:
        raise HarmonyCompilerErrorCollection([e.token])


def do_compile(filenames: List[str], consts: List[str], mods: List[str], interface: List[str]):
    for c in consts:
        try:
            i = c.index("=")
            parse_constant(c[0:i], c[i + 1:])
        except (IndexError, ValueError):
            raise HarmonyCompilerError(
                message="Usage: -c C=V to define a constant"
            )

    for m in mods:
        try:
            i = m.index("=")
            legacy_harmony.modules[m[0:i]] = m[i + 1:]
        except (IndexError, ValueError):
            raise HarmonyCompilerError(
                message="Usage: -m module=version to specify a module version"
            )

    scope = Scope(None)
    code = Code()
    code.append(FrameOp(("__init__", None, None, None), []))
    for fname in filenames:
        load_file(str(fname), scope, code)
    if interface is not None:
        load_string("def __iface__(): result = (%s)" %
                    interface, scope, code, "interface")

    code.append(ReturnOp())  # to terminate "__init__" process

    # Analyze liveness of variables
    newcode = code.liveness()

    newcode.link()
    optimize(newcode)
    return newcode, scope


args = argparse.ArgumentParser("harmony")
args.add_argument("-a", action="store_true",
                  help="list machine code (with labels)")
args.add_argument("-A", action="store_true",
                  help="list machine code (without labels)")
args.add_argument("-B", type=str, nargs=1,
                  help="check against the given behavior")
args.add_argument("-p", "--parse", action="store_true",
                  help="parse code without running")
args.add_argument("-c", "--const", action='append', type=str,
                  metavar="name=value", help="define a constant")
args.add_argument("-d", action='store_true',
                  help="htmldump full state into html file")
args.add_argument("--module", "-m", action="append", type=str,
                  metavar="module=version", help="select a module version")
args.add_argument("-i", "--intf", type=str, metavar="expr",
                  help="specify in interface function")
args.add_argument("-s", action="store_true",
                  help="silent (do not print periodic status updates)")
args.add_argument("-v", "--version", action="store_true",
                  help="print version number")
args.add_argument("-f", action="store_true",
                  help="run with internal model checker (not supported)")
args.add_argument("-o", action='append', type=pathlib.Path,
                  help="specify output file (.hvm, .hco, .hfa, .htm. .tla, .png, .gv)")
args.add_argument("-j", action="store_true",
                  help="list machine code in JSON format")
args.add_argument("--noweb", action="store_true", default=False,
                  help="do not automatically open web browser")
args.add_argument("--suppress", action="store_true",
                  help="generate less terminal output")

# Internal flags
args.add_argument("-b", action="store_true", help=argparse.SUPPRESS)
args.add_argument("--cf", action="append", type=str, help=argparse.SUPPRESS)

args.add_argument("files", metavar="harmony-file",
                  type=pathlib.Path, nargs='*', help="files to compile")


def main():
    ns = args.parse_args()

    if ns.f:
        # remove the first instance of "-f" from the legacy model checker
        sys.argv.remove("-f")
        legacy_harmony.main()
        return 0

    if ns.version:
        print("Version:", harmony_model_checker.__package__,
              harmony_model_checker.__version__)
        return 0

    check_version.check_outdated(
        harmony_model_checker.__package__, harmony_model_checker.__version__)

    consts: List[str] = ns.const or []
    interface: Optional[str] = ns.intf
    mods: List[str] = ns.module or []
    parse_code_only: bool = ns.parse
    charm_flag = True

    print_code: Optional[str] = None
    if ns.a:
        print_code = "verbose"
        charm_flag = False
    if ns.A:
        print_code = "terse"
        charm_flag = False
    if ns.j:
        print_code = "json"
        charm_flag = False
    if ns.f:
        charm_flag = False

    block_flag: bool = ns.b
    fulldump: bool = ns.d
    legacy_harmony.silent = ns.s

    output_files: Dict[str, Optional[str]] = {
        "hfa": None,
        "htm": None,
        "hco": None,
        "hvm": None,
        "png": None,
        "tla": None,
        "gv":  None
    }
    for p in (ns.o or []):
        # The suffix includes the dot if it exists.
        # Otherwise, it is an empty string.
        suffix = p.suffix[1:]
        if suffix not in output_files:
            print(f"Unknown file suffix on {p}")
            return 1
        if output_files[suffix] is not None:
            print(f"Duplicate suffix '.{suffix}'")
            return 1
        output_files[suffix] = str(p)

    suppress_output = ns.suppress

    behavior = None
    charm_options = ns.cf or []
    if ns.B:
        charm_options.append("-B" + ns.B)
        behavior = ns.B

    open_browser = not ns.noweb

    filenames: List[pathlib.Path] = ns.files
    if not filenames:
        args.print_help()
        return 1
    for f in filenames:
        if not f.exists():
            print(f"harmony: error: file named '{f}' does not exist.")
            return 1
    stem = str(filenames[0].parent / filenames[0].stem)

    if output_files["hvm"] is None:
        output_files["hvm"] = stem + ".hvm"
    if output_files["hco"] is None:
        output_files["hco"] = stem + ".hco"
    if output_files["htm"] is None:
        output_files["htm"] = stem + ".htm"
    if output_files["png"] is not None and output_files["gv"] is None:
        output_files["gv"] = stem + ".gv"

    print("Phase 1: compile Harmony program to bytecode")
    try:
        code, scope = do_compile(filenames, consts, mods, interface)
    except (HarmonyCompilerErrorCollection, HarmonyCompilerError) as e:
        if isinstance(e, HarmonyCompilerErrorCollection):
            errors = e.errors
        else:
            errors = [e.token]

        if parse_code_only:
            data = dict(errors=[e._asdict() for e in errors], status="error")
            with open(output_files["hvm"], "w") as fp:
                json.dump(data, fp)
        else:
            for e in errors:
                print(f"Line {e.line}:{e.column} at {e.filename}, {e.message}")
                print()
        return 1

    if parse_code_only:
        with open(output_files["hvm"], "w") as f:
            f.write(json.dumps({"status": "ok"}))
        return

    if output_files["tla"] is not None:
        with open(output_files["tla"], "w") as f:
            tla_translate(f, code, scope)

    # Analyze liveness of variables
    if charm_flag:
        # see if there is a configuration file
        with open(output_files["hvm"], "w") as fd:
            dumpCode("json", code, scope, f=fd)

        if parse_code_only:
            return 0

        print("Phase 2: run the model checker")
        r = charm.run_model_checker(
            *charm_options,
            "-o" + output_files["hco"],
            output_files["hvm"]
        )
        if r != 0:
            print("charm model checker failed")
            return r
        b = Brief()
        b.run(output_files, behavior)
        gh = GenHTML()
        gh.run(output_files)
        if not suppress_output:
            p = pathlib.Path(output_files["htm"]).resolve()
            url = "file://" + str(p)
            print("open " + url + " for more information", file=sys.stderr)
            if open_browser:
                webbrowser.open(url)
        return 0

    if print_code is None:
        nodes, bad_node = run(code, scope.labels, block_flag)
        if bad_node is not None:
            if not legacy_harmony.silent:
                htmldump(nodes, code, scope, bad_node, fulldump, False)
            return 1
    else:
        dumpCode(print_code, code, scope)
