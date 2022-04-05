from antlr4 import *

from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection

import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.harmony.harmony import Scope, Code, State, BlockAST, AST
from harmony_model_checker.parser.antlr_rule_visitor import HarmonyVisitorImpl
from harmony_model_checker.parser.HarmonyParser import HarmonyParser
from harmony_model_checker.parser.HarmonyErrorListener import HarmonyLexerErrorListener, HarmonyParserErrorListener
from harmony_model_checker.parser.HarmonyLexer import HarmonyLexer
from harmony_model_checker.harmony.ops import *

import os

from typing import List

def _build_input_stream(**kwargs) -> InputStream:
    try:
        filename = kwargs.get('filename', None)
        str_value = kwargs.get('str_value', None)
        if filename is not None:
            return FileStream(filename, 'utf-8')
        elif str_value is not None:
            return InputStream(str_value)
    except UnicodeDecodeError as e:
        lexeme = str(e.args[1][e.start:e.end]) # e.args[0] is the encoding name, and e.args[1] contains the bytes being parsed.
        raise HarmonyCompilerError(
            message=e.reason,
            filename=filename,
            line=1,
            column=1,
            lexeme=lexeme
        )
    raise ValueError("Cannot build input stream without a source")


def _build_parser(progam_input: InputStream, lexer_error_listener=None, parser_error_listener=None):
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


def _load_string(string, scope: Scope, code: Code, filename="<string-code>"):
    legacy_harmony.namestack.append(filename)
    ast = _parse_string(string, filename)
    for mod in ast.getImports():
        _do_import(scope, code, mod)
    # method names and label names get a temporary value
    # they are filled in with their actual values after compilation
    # TODO.  Look for duplicates?
    for ((lexeme, file, line, column), lb) in ast.getLabels():
        scope.names[lexeme] = ("constant", (lb, file, line, column))

    ast.compile(scope, code)
    legacy_harmony.namestack.pop()


def _load_file(filename: str, scope: Scope, code: Code):
    if filename in legacy_harmony.files:
        return
    legacy_harmony.namestack.append(filename)
    with open(filename, "r", encoding='utf-8') as f:
        legacy_harmony.files[filename] = f.read().split("\n")

    ast = _parse(filename)
    if ast is None:
        raise HarmonyCompilerError(
            message="Unknown error: unable to parse Harmony file",
            filename=filename
        )

    for mod in ast.getImports():
        _do_import(scope, code, mod)

    # method names and label names get a temporary value
    # they are filled in with their actual values after compilation
    # TODO.  Look for duplicates?
    for ((lexeme, file, line, column), lb) in ast.getLabels():
        scope.names[lexeme] = ("constant", (lb, file, line, column))

    ast.compile(scope, code)
    legacy_harmony.namestack.pop()


def _do_import(scope: Scope, code: Code, module):
    (lexeme, file, line, column) = module
    # assert lexeme not in scope.names        # TODO
    if lexeme not in legacy_harmony.imported:
        # Obsolete:
        # code.append(PushOp((legacy_harmony.novalue, file, line, column)))
        # code.append(StoreOp(module, module, None))

        # module name replacement with -m flag
        modname = legacy_harmony.modules.get(lexeme, lexeme)

        # create a new scope
        scope2 = Scope(None)
        scope2.prefix = lexeme
        scope2.labels = scope.labels
        scope2.inherit = True

        found = False
        install_path = os.path.dirname(os.path.realpath(__file__))
        for directory in [os.path.dirname(legacy_harmony.namestack[-1]), os.path.join(install_path, "modules"), "."]:
            filename = os.path.join(directory, modname + ".hny")
            if os.path.exists(filename):
                _load_file(filename, scope2, code)
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


def _parse_constant(name: str, value: str):
    filename = "<constant argument>"
    _input = _build_input_stream(str_value=value)
    parser = _build_parser(_input)
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


def _parse_string(string: str, filename: str = "<string-code>") -> BlockAST:
    _input = _build_input_stream(str_value=string)
    parser = _build_parser(_input)
    visitor = HarmonyVisitorImpl(filename)

    tree = parser.program()
    return visitor.visit(tree)


def _parse(filename: str) -> BlockAST:
    _input = _build_input_stream(filename=filename)
    error_listener = HarmonyParserErrorListener(filename)
    lexer_error_listener = HarmonyLexerErrorListener(filename)
    parser = _build_parser(
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


def parse(filename: str) -> AST:
    return _parse(filename)


def parse_string(string: str) -> AST:
    return _parse_string(string)


def do_compile(fname: str, consts: List[str], mods: List[str], interface: List[str]):
    for c in consts:
        try:
            i = c.index("=")
            _parse_constant(c[0:i], c[i + 1:])
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
    scope.inherit = True
    code = Code()
    code.append(FrameOp(("__init__", None, None, None), []))
    _load_file(str(fname), scope, code)
    if interface is not None:
        _load_string("def __iface__(): result = (%s)" %
                    interface, scope, code, "interface")

    code.append(ReturnOp())  # to terminate "__init__" process

    unused_constant_def = legacy_harmony.constants.keys() - legacy_harmony.used_constants
    unused_module_def = legacy_harmony.modules.keys() - legacy_harmony.imported.keys()
    if len(unused_constant_def) > 0:
        raise HarmonyCompilerError(
            message="The following constants were defined from the command line but not used: " + ', '.join(unused_constant_def),
            filename=fname,
            line=0,
            column=0,
            lexeme="",
        )
    if len(unused_module_def) > 0:
        raise HarmonyCompilerError(
            message="The following modules were defined from the command line but not used: " + ', '.join(unused_module_def),
            filename=fname,
            line=0,
            column=0,
            lexeme="",
        )

    # Analyze liveness of variables
    newcode = code.liveness()

    newcode.link()
    legacy_harmony.optimize(newcode)
    return newcode, scope
