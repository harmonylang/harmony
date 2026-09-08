from typing import Dict, List, Optional
import json
import pathlib
import webbrowser
import sys
import os
import argparse
import hashlib

from antlr4 import * # type: ignore

import harmony_model_checker
from harmony_model_checker.config import settings
from harmony_model_checker import charm # type: ignore
from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection
import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.harmony.genhtml import GenHTML
from harmony_model_checker.harmony.brief import Brief
from harmony_model_checker.harmony.verbose import Verbose
from harmony_model_checker.compile import do_compile


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


def _precheck_cleanup_output_files(output_files):
    # Mirrors handle_hny's own cleanup of stale output files from a
    # previous run - needed here too since a blocking Phase 0 finding
    # exits before handle_hny ever gets to do it itself.
    for suffix, file in output_files.items():
        if file is not None:
            try:
                os.remove(file)
            except:
                pass


def handle_precheck(ns, output_files, parse_code_only, filename):
    """Phase 0: run the standalone identifier checker over the program
    before the real (ANTLR-based) compiler ever sees it. This is an
    early, additional pass, never a replacement for the pipeline below:
      - if checker.py/parser.py can't be found, or this pass hits
        anything unexpected, it's silently skipped (see the try/except
        around the whole pass) - a bug in a still-evolving checker
        should never block a program the real compiler would otherwise
        accept;
      - if the program doesn't even parse under checker.py's own
        (still-evolving, hand-written) parser, that's printed as a
        note, not a hard error - its grammar coverage isn't guaranteed
        to fully match the ANTLR grammar yet;
      - a 'cannot resolve' import/module error is also only a note,
        since this pass's own module resolution (_precheck_module_map)
        doesn't perfectly replicate the real compiler's per-file-
        relative one;
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

    parse_failed = (
        len(program.errors) == 1
        and program.errors[0].message.startswith("program does not parse:")
    )

    blocking = []
    advisory = []
    for err in program.errors:
        if parse_failed or err.message.startswith("cannot resolve '"):
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
    _precheck_cleanup_output_files(output_files)
    if parse_code_only:
        data = dict(errors=[_to_error_dict(e) for e in blocking], status="error")
        with open(output_files["hvm"], "w", encoding='utf-8') as fp:
            json.dump(data, fp)
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
args.add_argument("-B", type=str, help="check against the given behavior")
args.add_argument("-d", "--direct", action="store_true",
                  help="run directly without model checking")
args.add_argument("-p", "--parse", action="store_true",
                  help="parse code without running")
args.add_argument("-c", "--const", action='append', type=str,
                  metavar="name=value", help="define a constant")
args.add_argument("-D", action="store_true",
                  help="dump Kripke graph")
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
args.add_argument("-o", action='append', type=pathlib.Path,
                  help="specify output file (.hvm, .hco, .hfa, .htm. .tla, .tex, .png, .gv)")
args.add_argument("-j", action="store_true",
                  help="list machine code in JSON format")
args.add_argument("-w", type=str, help="set number of workers")
args.add_argument("-t", type=str, help="set maximum model check timeout")
args.add_argument("-X", type=str, help="set maximum analysis timeout per phase")
args.add_argument("--noweb", action="store_true", default=False,
                  help="do not automatically open web browser")
args.add_argument("--suppress", action="store_true",
                  help="generate less terminal output")
args.add_argument("--config", action="store_true",
                  help="get or set configuration value. "
                       "Use --config <key> to get the value of a setting. "
                       "Use --config <key> <value> to set the value of a setting")

# Internal flags
args.add_argument("--cf", action="append", type=str, help=argparse.SUPPRESS)
args.add_argument("args", metavar="args", type=str, nargs='*', help="arguments")

def handle_hny(ns, output_files, parse_code_only, filenames):
    for suffix, file in output_files.items():
        if file is not None:
            try:
                os.remove(file)
            except:
                pass

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
            with open(output_files["hvm"], "w", encoding='utf-8') as fp:
                json.dump(data, fp)
        else:
            for e in errors:
                print(f"Line {e.line}:{e.column} at {e.filename}, {e.message}")
                print()
        exit(1)

    if parse_code_only:
        with open(output_files["hvm"], "w", encoding='utf-8') as f:
            f.write(json.dumps({"status": "ok"}))
        exit()

    if output_files["tla"] is not None:
        with open(output_files["tla"], "w", encoding='utf-8') as f:
            legacy_harmony.tla_translate(f, code, scope)

    if output_files["tex"] is not None:
        with open(output_files["tex"], "w", encoding='utf-8') as f:
            legacy_harmony.tex_output(f, code, scope)

    return code, scope

def handle_hvm(ns, output_files, parse_code_only, code, scope, behavior):
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
    if ns.D:
        charm_options.append("-D")
    if ns.R:
        charm_options.append("-R")
    if ns.U:
        charm_options.append("-U")
    if ns.W:
        charm_options.append("-c")

    # see if there is a configuration file
    if code is not None:
        with open(output_files["hvm"], "w", encoding='utf-8') as fd:
            legacy_harmony.dumpCode("json", code, scope, f=fd)

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
    if ns.quick:
        return

    suppress_output = ns.suppress
    disable_browser = settings.values.disable_web or ns.noweb

    b = Brief()
    b.run(output_files, behavior)
    vb = Verbose()
    vb.run(output_files)
    gh = GenHTML()
    gh.run(output_files)
    if not suppress_output:
        print()
        p = pathlib.Path(output_files["htm"]).resolve()
        url = "file://" + str(p)
        print("open " + url + " for detailed information", file=sys.stderr)
        if not disable_browser:
            webbrowser.open(url)
    # exit as minify may still be running
    print(flush=True, end="")
    print(file=sys.stderr, flush=True, end="")
    os._exit(0)

def handle_version(_: argparse.Namespace):
    print("Version:", harmony_model_checker.__package__,
          harmony_model_checker.__version__)
    return 0


def handle_config(ns: argparse.Namespace):
    if len(ns.args) == 0:
        print("Configuration settings:")
        for k, v in settings.values._asdict().items():
            print(f"    {k}: {v}")
        print("Use --config <key> to get the value of a setting.\nUse --config <key> <value> to set the value of a setting")
        return 0
    key = ns.args[0]
    try:
        if len(ns.args) > 1:
            value = ns.args[1]
            settings.update_settings_file(key, value)
        else:
            print(settings.get_settings_value(key))
    except AttributeError:
        print(f"'{key}' is not a valid configuration setting")
        return 1
    except ValueError as e:
        print(
            f"Value '{e.args[0]}' is not a valid value for configuration setting '{key}'")
        return 1
    return 0


def main():
    ns = args.parse_args()

    if ns.version:
        return handle_version(ns)

    if ns.config:
        return handle_config(ns)

    parse_code_only: bool = ns.parse
    legacy_harmony.silent = ns.s

    output_files: Dict[str, Optional[str]] = {
        "hfa": None,
        "htm": None,
        "hvb": None,
        "hco": None,
        "hvm": None,
        "png": None,
        "tla": None,
        "tex": None,
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

    filename = None
    behavior_file = ns.B if ns.B else None
    for f in ns.args:
        name = pathlib.Path(f)
        if not name.exists():
            print(f"harmony: error: file named '{name}' does not exist.")
            return 1
        file_type = name.suffix
        if file_type == '.hfa':
            if behavior_file != None:
                print(f"harmony: error: duplicate behavior file.")
                return 1
            behavior_file = f
        elif filename == None:
            filename = name
        else:
            print(f"harmony: error: multiple input files.")
            args.print_help()
            return 1

    if filename == None:
        print(f"harmony: no input file")
        args.print_help()
        return 1

    stem = str(filename.parent / filename.stem)
    input_file_type = filename.suffix

    # generate a "run id"
    f1 = [str(filename)]
    f2 = ["" if behavior_file == None else behavior_file]
    f3 = [] if ns.const == None else sorted(ns.const)
    f4 = [] if ns.module == None else sorted(ns.module)
    ff = ",".join(f1 + f2 + f3 + f4)
    sha3 = hashlib.sha3_256()
    sha3.update(ff.encode('utf-8'))
    runid = sha3.hexdigest()[:8]

    if output_files["hvm"] is None:
        output_files["hvm"] = stem + ".hvm"
    if output_files["hco"] is None:
        output_files["hco"] = stem + ".hco"
    if output_files["htm"] is None:
        output_files["htm"] = stem + ".htm"
    if output_files["hvb"] is None:
        output_files["hvb"] = stem + ".hvb"
    if output_files["hfa"] is None:
        output_files["hfa"] = stem + "-" + runid + ".hfa"
    if output_files["png"] is not None and output_files["gv"] is None:
        output_files["gv"] = stem + "-" + runid + ".gv"
    if output_files["png"] is None:
        output_files["png"] = stem + "-" + runid + ".png"

    # print(output_files)

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

    # Handle different Harmony compilation stages
    if input_file_type == ".hny":
        handle_precheck(ns, output_files, parse_code_only, str(filename))
        code, scope = handle_hny(ns, output_files, parse_code_only, str(filename))
        if charm_flag:
            handle_hvm(ns, output_files, parse_code_only, code, scope, behavior_file)
            handle_hco(ns, output_files, behavior_file)
        else:
            print("Skipping Phases 2-5...", flush=True)
            legacy_harmony.dumpCode(print_code, code, scope)

    if input_file_type == ".hvm":
        print("Skipping Phase 1...", flush=True)
        handle_hvm(ns, output_files, parse_code_only, None, None, behavior_file)
        handle_hco(ns, output_files, behavior_file)

    if input_file_type == ".hco":
        print("Skipping Phases 1-4...", flush=True)
        handle_hco(ns, output_files, behavior_file)
