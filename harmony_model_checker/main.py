from typing import Dict, List, Optional
import json
import pathlib
import webbrowser
import sys
import os
import argparse
import hashlib
import shutil
import tempfile
import shlex
import contextlib
from datetime import datetime

from antlr4 import * # type: ignore

import harmony_model_checker
from harmony_model_checker import charm # type: ignore
from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection
import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.harmony.genhtml import GenHTML
from harmony_model_checker.harmony.brief import Brief
from harmony_model_checker.harmony.verbose import Verbose
from harmony_model_checker.compile import do_compile
from harmony_model_checker.harmony.runinfo import run_info_comment, source_name


# ---------------------------------------------------------------------------
# Optional preprocessing pass (Phase 0): a hand-written, still-evolving
# identifier checker (checker.py, built on its own recursive-descent
# parser.py) living inside this package. It re-parses the program and
# checks that every name used is declared somewhere reachable, before
# its use - catching undeclared/misused names, illegal shadowing, and
# '?'/assignment misuse earlier, and with more specific messages, than
# the ANTLR-based pipeline below currently gives (see checker.py's own
# module docstring for the full rules). It never replaces that pipeline
# - the ANTLR-based compile below is still the real compiler and always
# gets the final say; if this pass can't even be imported, it's
# silently skipped rather than blocking anything - see handle_precheck.
# ---------------------------------------------------------------------------
try:
    from harmony_model_checker import checker as _precheck  # type: ignore
except Exception:
    _precheck = None


def _precheck_resolve_module_file(modname, source_dir):
    """Mirrors harmony_model_checker.compile._do_import's own search
    order for one module name: the importing file's own directory, this
    package's bundled modules directory (checker.py's own
    DEFAULT_MODULE_DIR - it lives right alongside 'modules/' in this
    package, so that default is already correct here), then the current
    working directory."""
    for directory in (source_dir, _precheck.DEFAULT_MODULE_DIR, "."):
        if directory is None:
            continue
        candidate = os.path.join(directory, modname + ".hny")
        if os.path.isfile(candidate):
            return candidate
    return None


def _precheck_module_map(mods, source_dir):
    """Builds checker.py's module_map (module name -> file path) from
    the CLI's own '-m orig=replacement' entries. do_compile treats each
    one as "when the program imports orig, actually load replacement's
    file instead" (see harmony_model_checker.compile.do_compile and
    _do_import, which resolves 'replacement' the same way an ordinary
    import is resolved) - so this looks up replacement's own file (same
    search order) and maps it under orig's name. An entry whose
    replacement file can't be found here is simply left out - checker.py
    then falls back to its own default (looking for orig.hny itself),
    which is no worse than not knowing about '-m' at all, just less
    precise for that one name."""
    module_map = {}
    for m in (mods or []):
        if "=" not in m:
            continue   # malformed - do_compile reports this properly itself
        orig, _, replacement = m.partition("=")
        path = _precheck_resolve_module_file(replacement, source_dir)
        if path is not None:
            module_map[orig] = path
    return module_map


def _precheck_extra_consts(consts):
    """Names bound by the CLI's own '-c NAME=VALUE' entries - these are
    constants as far as identifier checking is concerned, whether or
    not the program's own source also writes 'const NAME = ...' (see
    checker.check_identifiers's own extra_consts parameter, and
    do_compile's matching '-c' handling below in handle_hny)."""
    names = []
    for c in (consts or []):
        if "=" not in c:
            continue   # malformed - do_compile reports this properly itself
        name, _, _value = c.partition("=")
        names.append(name)
    return names


def write_parse_status(output_files, data):
    """With -p, the parse result (a small JSON status object) goes to
    the .hvm file named with -o, or to stdout if there is none."""
    dest = output_files["hvm"]
    if dest is None:
        # stdout itself is redirected to stderr in -p mode (see run_stages)
        print(json.dumps(data), file=sys.__stdout__, flush=True)
    else:
        with open(dest, "w", encoding='utf-8') as fp:
            json.dump(data, fp)


def handle_precheck(ns, output_files, parse_code_only, filename):
    """Phase 0: run the standalone identifier checker over the program
    before the real (ANTLR-based) compiler ever sees it. This is an
    early, additional pass, never a replacement for the pipeline below:
      - if checker.py/harmony_parser.py can't be found, or this pass
        hits anything unexpected, it's silently skipped (see the
        try/except around the whole pass) - a bug in a still-evolving
        checker should never block a program the real compiler would
        otherwise accept;
      - if the program doesn't even parse under checker.py's own
        (still-evolving, hand-written) parser, that's now a hard error
        too, stopping the run right here, same as any other Phase 0
        finding - harmony_parser.py has been exercised heavily enough
        (243 checker tests, 166 parser cases) that a genuine syntax
        rejection is far more likely to be real than a coverage gap,
        and a parse failure's own message is usually far more precise
        than whatever confusing, lower-level error Phase 1 would
        eventually produce for the same program (see e.g. '?'-operand
        shape errors);
      - a 'cannot resolve' import/module error is still only a note,
        since this pass's own module resolution (_precheck_module_map)
        doesn't perfectly replicate the real compiler's per-file-
        relative one - that mismatch is specifically about FINDING a
        file, not about the program's own syntax or identifiers, so it
        stays advisory-only;
      - every other identifier problem - an undeclared name, illegal
        shadowing, illegal '?'/assignment-target use, and so on - is
        specific and self-contained enough (it doesn't depend on
        cross-file module resolution) to report as a hard error, in
        the same format the ANTLR pipeline's own errors use below, and
        stops the run right here: a program with a real undeclared
        name or illegal shadow is going to fail one way or another, and
        this pass explains why more precisely than Phase 1 currently
        does.
    """
    if _precheck is None:
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            document = f.read()

        source_dir = os.path.dirname(os.path.abspath(filename))
        module_map = _precheck_module_map(ns.module, source_dir)
        extra_consts = _precheck_extra_consts(ns.const)

        program = _precheck.check_identifiers(
            document,
            module_map=module_map,
            source_label=filename,
            source_dir=source_dir,
            extra_consts=extra_consts,
            # default_module_dir is deliberately omitted - checker.py's
            # own default is already correct (see
            # _precheck_resolve_module_file's docstring above).
        )
    except Exception as e:
        print(f"* Phase 0: identifier pre-check skipped ({e})", flush=True)
        return

    if not program.errors:
        return

    blocking = []
    advisory = []
    for err in program.errors:
        if err.message.startswith("cannot resolve '"):
            advisory.append(err)
        else:
            blocking.append(err)

    for err in advisory:
        line, column = _precheck.offset_to_line_col(document, err.start)
        print(f"note: Line {line}:{column} at {filename}, {err.message}", flush=True)

    if not blocking:
        return

    def _to_error_dict(err):
        line, column = _precheck.offset_to_line_col(document, err.start)
        # Matches ErrorToken's own field names (exception.py) so this
        # slots into the same JSON shape the ANTLR pipeline's own
        # parse-code-only error output already uses.
        return dict(line=line, column=column, message=err.message,
                    lexeme="", filename=filename, is_eof_error=False)

    print("* Phase 0: identifier pre-check found problems", flush=True)
    if parse_code_only:
        data = dict(errors=[_to_error_dict(e) for e in blocking], status="error")
        write_parse_status(output_files, data)
    else:
        for err in blocking:
            line, column = _precheck.offset_to_line_col(document, err.start)
            print(f"Line {line}:{column} at {filename}, {err.message}")
            print()
    exit(1)


args = argparse.ArgumentParser(
    "harmony", description="Harmony programming language compiler and model checker")
args.add_argument("-a", action="store_true",
                  help="list machine code (with labels)")
args.add_argument("-b", action="store_true",
                  help="enable behavior subset check")
args.add_argument("-T", action="store_true",
                  help="print timing info")
args.add_argument("-A", action="store_true",
                  help="list machine code (without labels)")
# Same as giving the behavior file (.hfa) as an extra argument; kept
# for compatibility but no longer documented.
args.add_argument("-B", type=str, help=argparse.SUPPRESS)
args.add_argument("-d", "--direct", action="store_true",
                  help="run directly without model checking")
args.add_argument("-p", "--parse", action="store_true",
                  help="only check the program for compile errors; the result "
                       "is a JSON status, written to the .hvm file given with -o "
                       "or else to stdout")
args.add_argument("-c", "--const", action='append', type=str,
                  metavar="name=value", help="define a constant")
# Replaced by -o <file>.kripke.gv and -o <file>.dump (undocumented,
# for debugging Harmony itself); kept only to explain that.
args.add_argument("-D", action="store_true", help=argparse.SUPPRESS)
args.add_argument("-W", action="store_true",
                  help="suppress busy waiting check")
args.add_argument("-R", action="store_true",
                  help="suppress race condition warnings")
args.add_argument("-U", action="store_true",
                  help="do not pin workers")
args.add_argument("--module", "-m", action="append", type=str,
                  metavar="module=version", help="select a module version")
args.add_argument("-i", "--intf", type=str, metavar="expr",
                  help="specify an interface function")
args.add_argument("-s", action="store_true",
                  help="silent (do not print periodic status updates)")
args.add_argument("-v", "--version", action="store_true",
                  help="print version number")
args.add_argument("--quick", action="store_true",
                  help="no post-model-check analysis")
args.add_argument("-o", action='append', type=pathlib.Path, metavar="file",
                  help="write an output file; the suffix selects the kind "
                       "(.hvm, .hco, .hfa, .md, .htm, .hvb, .png, .gv, .tla, .tex). "
                       "May be repeated. Without -o, no files are written")
args.add_argument("-j", action="store_true",
                  help="list machine code in JSON format")
args.add_argument("-w", type=str, help="set number of workers")
args.add_argument("-t", type=str, help="set maximum model check timeout")
args.add_argument("-X", type=str, help="set maximum analysis timeout per phase")
args.add_argument("--browse", action="store_true", default=False,
                  help="open the detailed HTML output in a web browser")
# The browser is no longer opened by default, so --noweb has no effect.
# It is still accepted because existing tools (e.g., the VS Code
# extension) pass it.
args.add_argument("--noweb", action="store_true", default=False,
                  help=argparse.SUPPRESS)
args.add_argument("--suppress", action="store_true",
                  help="generate less terminal output")

# Internal flags
args.add_argument("--cf", action="append", type=str, help=argparse.SUPPRESS)
args.add_argument("args", metavar="args", type=str, nargs='*', help="arguments")

def handle_hny(ns, output_files, parse_code_only, filenames, config=None):
    print("* Phase 1: compile Harmony program to bytecode", flush=True)

    consts: List[str] = ns.const or []
    interface: Optional[str] = ns.intf
    mods: List[str] = ns.module or []

    try:
        code, scope = do_compile(filenames, consts, mods, interface)
    except (HarmonyCompilerErrorCollection, HarmonyCompilerError) as err:
        if isinstance(err, HarmonyCompilerErrorCollection):
            errors = err.errors
        else:
            errors = [err.token]

        if parse_code_only:
            data = dict(errors=[e._asdict() for e in errors], status="error")
            write_parse_status(output_files, data)
        else:
            for e in errors:
                print(f"Line {e.line}:{e.column} at {e.filename}, {e.message}")
                print()
        exit(1)

    if parse_code_only:
        write_parse_status(output_files, {"status": "ok"})
        exit()

    if output_files["tla"] is not None:
        with open(output_files["tla"], "w", encoding='utf-8') as f:
            print(run_info_comment(config, "\\*"), end="", file=f)
            legacy_harmony.tla_translate(f, code, scope)

    if output_files["tex"] is not None:
        with open(output_files["tex"], "w", encoding='utf-8') as f:
            print(run_info_comment(config, "%"), end="", file=f)
            legacy_harmony.tex_output(f, code, scope)

    return code, scope

def handle_hvm(ns, output_files, parse_code_only, code, scope, behavior, config=None):
    charm_options = ns.cf or []
    if behavior != None:
        charm_options.append("-B" + behavior)
    if ns.b:
        charm_options.append("-b")
    if ns.T:
        charm_options.append("-T")
    if ns.w:
        charm_options.append("-w" + ns.w)
    if ns.t:
        charm_options.append("-t" + ns.t)
    if ns.X:
        charm_options.append("-X" + ns.X)
    for debug_output in ("kripke.gv", "dump"):
        if output_files.get(debug_output) is not None:
            charm_options.append("-o" + output_files[debug_output])
    if ns.R:
        charm_options.append("-R")
    if ns.U:
        charm_options.append("-U")
    if ns.W:
        charm_options.append("-c")

    if code is not None:
        with open(output_files["hvm"], "w", encoding='utf-8') as fd:
            legacy_harmony.dumpCode("json", code, scope, f=fd, config=config)

    if parse_code_only:
        exit()

    if ns.direct:
        # print("* Phase 2: run", flush=True)
        charm_options.append("-d")
        r = charm.run_model_checker(
            *charm_options,
            output_files["hvm"]
        )
        if r != 0:
            print("charm failed")
            exit(r)
    else:
        # print("* Phase 2: run the model checker", flush=True)
        if "hfa" in output_files and output_files["hfa"] != None:
            r = charm.run_model_checker(
                *charm_options,
                "-o" + output_files["hco"],
                "-o" + output_files["hfa"],
                output_files["hvm"]
            )
        else:
            r = charm.run_model_checker(
                *charm_options,
                "-o" + output_files["hco"],
                output_files["hvm"]
            )
        if r != 0:
            print("charm model checker failed")
            exit(r)

def handle_hco(ns, output_files, behavior):
    """Produces the outputs from the .hco file.  Returns the issue found
    (None if unknown) and whether the program produces output."""
    if ns.quick:
        return None, False
    b = Brief()
    result = b.run(output_files, behavior)
    if output_files["hvb"] is not None:
        vb = Verbose()
        vb.run(output_files)
    if output_files["htm"] is not None:
        gh = GenHTML()
        gh.run(output_files)
    return result

def handle_version(_: argparse.Namespace):
    print("Version:", harmony_model_checker.__package__,
          harmony_model_checker.__version__)
    return 0


def main():
    ns = args.parse_args()

    if ns.version:
        return handle_version(ns)

    parse_code_only: bool = ns.parse
    legacy_harmony.silent = ns.s

    # Output files explicitly requested with -o, by suffix.  Nothing
    # else is written: intermediate files go in a private temporary
    # directory that is removed when Harmony exits.
    requested: Dict[str, pathlib.Path] = {}
    for p in (ns.o or []):
        # The suffix includes the dot if it exists.
        # Otherwise, it is an empty string.
        suffix = "kripke.gv" if p.name.endswith(".kripke.gv") else p.suffix[1:]
        if suffix not in OUTPUT_SUFFIXES:
            print(f"harmony: error: unknown file suffix on {p}")
            return 1
        if suffix in requested:
            print(f"harmony: error: duplicate suffix '.{suffix}'")
            return 1
        requested[suffix] = p

    # The input is a program (.hny, .hvm, or .hco) and optionally a
    # behavior to check it against: an .hfa file, or the .hco file of
    # an earlier run.  With two files the roles follow from the kinds
    # of file, so the order does not matter.
    inputs = []
    for f in ns.args:
        name = pathlib.Path(f)
        if not name.exists():
            print(f"harmony: error: file named '{name}' does not exist.")
            return 1
        inputs.append(name)
    behaviors = [ x for x in inputs if x.suffix == ".hfa" ]
    programs = [ x for x in inputs if x.suffix != ".hfa" ]
    if len(programs) == 2:
        compiled = [ x for x in programs if x.suffix == ".hco" ]
        others = [ x for x in programs if x.suffix in (".hny", ".hvm") ]
        if len(compiled) == 1 and len(others) == 1:
            behaviors += compiled
            programs = others
    if len(programs) > 1:
        print(f"harmony: error: multiple input files.")
        args.print_help()
        return 1
    behavior_file = ns.B if ns.B else None
    if len(behaviors) + (behavior_file is not None) > 1:
        print(f"harmony: error: duplicate behavior file.")
        return 1
    if behaviors:
        behavior_file = str(behaviors[0])
    filename = programs[0] if programs else None

    if filename == None:
        print(f"harmony: no input file")
        args.print_help()
        return 1

    stage = filename.suffix[1:]
    if stage not in ("hny", "hvm", "hco"):
        print(f"harmony: error: don't know what to do with '{filename}' "
              "(expected a .hny, .hvm, or .hco file)")
        return 1

    error = check_options(ns, stage, requested, filename, behavior_file)
    if error is not None:
        print(f"harmony: error: {error}")
        return 1

    tmpdir = tempfile.mkdtemp(prefix="harmony-")
    try:
        status, analyzed = run_stages(ns, stage, filename, behavior_file,
                                      requested, parse_code_only, tmpdir)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    if analyzed:
        # exit as minify may still be running
        print(flush=True, end="")
        print(file=sys.stderr, flush=True, end="")
        os._exit(status)
    return status


# Kinds of output file that can be requested with -o.
OUTPUT_SUFFIXES = ("hvm", "hco", "hfa", "md", "htm", "hvb", "png", "gv", "tla", "tex",
                   "kripke.gv", "dump")    # the last two are for debugging

# Options that only make sense when compiling a .hny file.
COMPILER_OPTIONS = (("-c", "const"), ("-m", "module"), ("-i", "intf"),
                    ("-p", "parse"), ("-a", "a"), ("-A", "A"), ("-j", "j"))

# Options that only make sense when model checking.
CHECKER_OPTIONS = (("-b", "b"), ("-B", "B"), ("-d", "direct"),
                   ("-R", "R"), ("-T", "T"), ("-U", "U"), ("-W", "W"),
                   ("-t", "t"), ("-w", "w"), ("-X", "X"))


def check_options(ns, stage, requested, filename, behavior_file):
    """Returns an error message if the options do not fit the input file,
    or None if they do."""
    if ns.D:
        return "-D has been replaced by -o <file>.kripke.gv and -o <file>.dump"
    if stage != "hny":
        for flag, attr in COMPILER_OPTIONS:
            if getattr(ns, attr):
                return (f"{flag} only applies when compiling a .hny file, "
                        f"but '{filename}' is already compiled")
        for suffix in ("tla", "tex"):
            if suffix in requested:
                return f"a .{suffix} file can only be produced from a .hny file"
    if stage == "hco":
        for flag, attr in CHECKER_OPTIONS:
            if getattr(ns, attr):
                return (f"{flag} only applies when model checking, "
                        f"but '{filename}' has already been model checked")
        if behavior_file is not None:
            return (f"a behavior file only applies when model checking, "
                    f"but '{filename}' has already been model checked")
        for suffix in ("kripke.gv", "dump"):
            if suffix in requested:
                return (f"a .{suffix} file is made while model checking, "
                        f"but '{filename}' has already been model checked")
    for dest in requested.values():
        if not dest.parent.resolve().is_dir():
            return f"cannot write '{dest}': directory '{dest.parent}' does not exist"
    inputs = [filename] + ([pathlib.Path(behavior_file)] if behavior_file else [])
    for dest in requested.values():
        for inp in inputs:
            if dest.resolve() == inp.resolve():
                return f"output file '{dest}' would overwrite input file '{inp}'"
    return None


def run_stages(ns, stage, filename, behavior_file, requested, parse_code_only, tmpdir):
    """Runs the pipeline .hny -> .hvm -> .hco -> (.md, .htm, ...) starting
    at the stage of the input file.  Intermediate files are created in
    tmpdir; requested outputs are copied to their destinations at the end.
    Returns (exit status, whether the analysis phase ran)."""

    # Working names for every kind of file, all inside the temporary
    # directory, except that the input file is used where it is.
    work = { s: os.path.join(tmpdir, filename.stem + "." + s) for s in OUTPUT_SUFFIXES }
    work[stage] = str(filename)

    # Only produce the files that are needed.  The HTML output embeds
    # the picture of the behavior, so it needs the .png (and the .gv
    # that it is made from).
    want_htm = "htm" in requested or ns.browse
    want_png = "png" in requested or want_htm
    output_files: Dict[str, Optional[str]] = {
        "hvm": work["hvm"],
        "hco": work["hco"],
        "hfa": work["hfa"],
        "md":  work["md"]  if "md"  in requested else None,
        "htm": work["htm"] if want_htm else None,
        "hvb": work["hvb"] if "hvb" in requested else None,
        "png": work["png"] if want_png else None,
        "gv":  work["gv"]  if want_png or "gv" in requested else None,
        "tla": work["tla"] if "tla" in requested else None,
        "tex": work["tex"] if "tex" in requested else None,
        "kripke.gv": work["kripke.gv"] if "kripke.gv" in requested else None,
        "dump": work["dump"] if "dump" in requested else None,
    }
    if parse_code_only:
        # With -p, the parse status goes to the .hvm output (or stdout).
        output_files["hvm"] = str(requested["hvm"]) if "hvm" in requested else None
        requested = { s: d for s, d in requested.items() if s != "hvm" }

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

    # The checker reads a behavior as an .hfa file; one given as the
    # .hco file of an earlier run is extracted from it first.
    if behavior_file is not None and behavior_file.endswith(".hco"):
        with open(behavior_file, encoding='utf-8') as f:
            top = json.load(f, strict=False)
        if "behavior" not in top:
            print(f"harmony: error: '{behavior_file}' contains no behavior "
                  "(the run found an issue, or it was made by an older version of Harmony)")
            return 1, False
        checker_behavior = os.path.join(tmpdir, "behavior.hfa")
        with open(checker_behavior, "w", encoding='utf-8') as f:
            json.dump(top["behavior"], f)
    else:
        checker_behavior = behavior_file

    # Warn about a behavior file that looks like the wrong one.
    if behavior_file is not None and stage in ("hny", "hvm"):
        if stage == "hny":
            constants = parse_pairs(ns.const)
        else:
            with open(filename, encoding='utf-8') as f:
                hvm_config = json.load(f, strict=False).get("config")
            constants = hvm_config.get("constants") if isinstance(hvm_config, dict) else None
        for warning in behavior_warnings(behavior_file, constants):
            print(f"harmony: warning: {warning}", file=sys.stderr, flush=True)

    analyzed = False
    issue, has_output = None, False
    if stage == "hny":
        config = make_config(ns, filename, behavior_file)
        # With -p, keep stdout for the JSON status alone.
        with (contextlib.redirect_stdout(sys.stderr) if parse_code_only
              else contextlib.nullcontext()):
            handle_precheck(ns, output_files, parse_code_only, str(filename))
            code, scope = handle_hny(ns, output_files, parse_code_only, str(filename), config)
        if not charm_flag:
            print("Skipping Phases 2-5...", flush=True)
            legacy_harmony.dumpCode(print_code, code, scope)
        else:
            handle_hvm(ns, output_files, parse_code_only, code, scope, checker_behavior, config)
            if not ns.direct:
                issue, has_output = handle_hco(ns, output_files, behavior_file)
                analyzed = True
    elif stage == "hvm":
        print("Skipping Phase 1...", flush=True)
        handle_hvm(ns, output_files, parse_code_only, None, None, checker_behavior)
        if not ns.direct:
            issue, has_output = handle_hco(ns, output_files, behavior_file)
            analyzed = True
    else:
        print("Skipping Phases 1-4...", flush=True)
        # The .hco file includes the behavior, which the outputs are made from.
        with open(filename, encoding='utf-8') as f:
            top = json.load(f, strict=False)
        if "behavior" in top:
            with open(work["hfa"], "w", encoding='utf-8') as f:
                json.dump(top["behavior"], f)
        del top
        issue, has_output = handle_hco(ns, output_files, behavior_file)
        analyzed = True

    status = deliver(requested, work, stage, filename)

    sys.stdout.flush()
    if analyzed and not ns.suppress:
        if "htm" in requested and os.path.exists(work["htm"]):
            url = pathlib.Path(requested["htm"]).resolve().as_uri()
            print("open " + url + " for detailed information", file=sys.stderr)
        elif ns.browse:
            pass
        elif issue is not None and issue != "No issues":
            print("use -o <file>.htm or --browse for details about the issue", file=sys.stderr)
        elif has_output and "png" not in requested and "gv" not in requested:
            print("use -o <file>.png, -o <file>.htm, or --browse to see "
                  "the program's output behavior", file=sys.stderr)

    if ns.browse and analyzed and os.path.exists(work["htm"]):
        if "htm" in requested:
            page = str(requested["htm"])
        else:
            # The temporary directory is about to be removed, so give the
            # browser a copy that stays behind.
            fd, page = tempfile.mkstemp(prefix="harmony-", suffix=".htm")
            os.close(fd)
            shutil.copyfile(work["htm"], page)
        webbrowser.open(pathlib.Path(page).resolve().as_uri())

    return status, analyzed


def parse_pairs(items):
    """Turns a list of "name=value" option arguments into a dict."""
    d = {}
    for item in items or []:
        name, _, value = item.partition("=")
        d[name] = value
    return d


def make_config(ns, filename, behavior_file):
    """How this run was invoked, recorded in the .hvm file (and from
    there in the .hco file and the outputs made from it)."""
    pairs = parse_pairs
    return {
        "harmony_version": harmony_model_checker.__version__,
        "command": shlex.join(["harmony"] + sys.argv[1:]),
        "input": str(filename),
        # File names are recorded as given; relative ones are relative to this.
        "cwd": os.getcwd(),
        "constants": pairs(ns.const),
        "modules": pairs(ns.module),
        "interface": ns.intf,
        "behavior": behavior_file,
        "behavior_origin": behavior_origin(behavior_file),
        "created": datetime.now().astimezone().isoformat(timespec="seconds"),
    }


def behavior_origin(behavior_file):
    """Where a behavior file came from, as recorded in it: the run that
    produced it (for an .hfa or .hco file made by this version of Harmony),
    or None if that is not known."""
    if behavior_file is None:
        return None
    try:
        with open(behavior_file, encoding='utf-8') as f:
            top = json.load(f, strict=False)
    except (OSError, ValueError):
        return None
    if behavior_file.endswith(".hco"):
        config = top.get("hvm", {}).get("config")
    else:
        config = top.get("config")
    if not isinstance(config, dict):
        return None
    return { k: config[k] for k in ("input", "command", "harmony_version", "created")
                if k in config }


def behavior_warnings(behavior_file, constants):
    """Looks for likely mistakes in the choice of behavior file, using
    what the file records about how it was made: source files that have
    changed since, and constants that differ from this run's (None if
    not known).  Returns a list of warnings."""
    try:
        with open(behavior_file, encoding='utf-8') as f:
            top = json.load(f, strict=False)
    except (OSError, ValueError):
        return []
    if behavior_file.endswith(".hco"):
        hvm = top.get("hvm", {})
        config = hvm.get("config")
        sources = { name: mod for name, mod in hvm.get("modules", {}).items()
                    if "sha256" in mod }
    else:
        config = top.get("config")
        sources = config.get("sources", {}) if isinstance(config, dict) else {}
    if not isinstance(config, dict):
        return [ f"'{behavior_file}' does not record how it was made (it is from "
                 "an older version of Harmony), so it cannot be checked for mistakes" ]

    warnings = []
    version = config.get("harmony_version")
    if version and version != harmony_model_checker.__version__:
        warnings.append(f"'{behavior_file}' was made with Harmony {version}; "
                        f"this is Harmony {harmony_model_checker.__version__}")

    # Relative file names are relative to the directory Harmony ran in when
    # the behavior was made, if that still exists (it does not if the file
    # came from another machine, say); otherwise to the current directory.
    cwd = config.get("cwd")
    base = cwd if isinstance(cwd, str) and os.path.isdir(cwd) else "."
    for name, src in sorted(sources.items()):
        path = src.get("file")
        if not path or src.get("library"):
            continue    # library modules change only with the version
        found = os.path.join(base, path)
        if not os.path.isfile(found):
            continue
        with open(found, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
        if digest != src.get("sha256"):
            warnings.append(f"'{path}' has changed since '{behavior_file}' was "
                            "made from it, so the behavior may be out of date")
    if constants is not None:
        theirs = config.get("constants") or {}
        def show(name, value):
            return f"{name}={value}" if value is not None else f"no -c for {name}"
        for name in sorted(set(theirs) | set(constants)):
            if theirs.get(name) != constants.get(name):
                warnings.append(f"'{behavior_file}' was made with {show(name, theirs.get(name))}, "
                                f"but this run has {show(name, constants.get(name))}")
    return warnings


def deliver(requested, work, stage, filename):
    """Copies each requested output from its working location to where
    the user asked for it.  Returns an exit status."""
    status = 0
    for suffix, dest in requested.items():
        src = work[suffix]
        if suffix == "hvm" and stage == "hco" and not os.path.exists(src):
            # A .hco file carries a copy of the bytecode it was made from.
            with open(filename, encoding='utf-8') as f:
                top = json.load(f, strict=False)
            if "hvm" in top:
                with open(src, "w", encoding='utf-8') as f:
                    json.dump(top["hvm"], f)
        if not os.path.exists(src):
            print(f"harmony: warning: no .{suffix} output was produced, "
                  f"so '{dest}' was not written", file=sys.stderr)
            status = 1
            continue
        if suffix == "hfa" and os.path.exists(work["hco"]):
            src = add_run_config(src, work["hco"])
        install_file(src, dest)
    return status


def add_run_config(hfa_file, hco_file):
    """The checker writes the behavior (.hfa) without saying where it came
    from.  Returns the name of a copy that includes the configuration of
    the run, the checker options, and the hashes of the source files, as
    recorded in the .hco file.  (The checker ignores the extra field when
    the file is used as a behavior.)"""
    with open(hco_file, encoding='utf-8') as f:
        top = json.load(f, strict=False)
    hvm = top.get("hvm", {})
    if "config" not in hvm:
        return hfa_file
    config = dict(hvm["config"])
    config["checker_options"] = top.get("checker_options", [])
    config["sources"] = { name: { "file": source_name(mod), "sha256": mod["sha256"],
                                  "library": bool(mod.get("library")) }
                          for name, mod in hvm.get("modules", {}).items()
                          if "sha256" in mod }
    with open(hfa_file, encoding='utf-8') as f:
        behavior = json.load(f, strict=False)
    result = hfa_file + ".config"
    with open(result, "w", encoding='utf-8') as f:
        json.dump({ "config": config, **behavior }, f, indent=2)
    return result


def install_file(src, dest):
    """Copies src to dest such that dest is replaced in one step: another
    Harmony run never sees a partially written file."""
    dest = pathlib.Path(dest)
    tmp = dest.with_name(f".{dest.name}.{os.getpid()}.tmp")
    try:
        shutil.copyfile(src, tmp)
        os.replace(tmp, dest)
    finally:
        if tmp.exists():
            tmp.unlink()
