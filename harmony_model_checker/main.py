from typing import Dict, List, Optional
import json
import pathlib
import webbrowser
import sys
import os
import argparse

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


args = argparse.ArgumentParser(
    "harmony", description="Harmony programming language compiler and model checker")
args.add_argument("-a", action="store_true",
                  help="list machine code (with labels)")
args.add_argument("-b", action="store_true",
                  help="enable behavior subset check")
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

def handle_hvm(ns, output_files, parse_code_only, code, scope):
    charm_options = ns.cf or []
    if ns.B:
        charm_options.append("-B" + ns.B)
    if ns.b:
        charm_options.append("-b")
    if ns.w:
        charm_options.append("-w" + ns.w)
    if ns.D:
        charm_options.append("-D")
    if ns.R:
        charm_options.append("-R")
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
        r = charm.run_model_checker(
            *charm_options,
            "-o" + output_files["hco"],
            output_files["hvm"]
        )
        if r != 0:
            print("charm model checker failed")
            exit(r)

def handle_hco(ns, output_files):
    if ns.quick:
        return

    suppress_output = ns.suppress

    behavior = None
    if ns.B:
        behavior = ns.B

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
        print("open " + url + " for detailed information, or use the HarmonyGUI", file=sys.stderr)
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

    if len(ns.args) != 1:
        print(f"harmony: error: invalid number of arguments ({len(ns.args)}). Provide 1 argument.")
        args.print_help()
        return 1

    filename = pathlib.Path(ns.args[0])
    if not filename.exists():
        print(f"harmony: error: file named '{filename}' does not exist.")
        return 1

    stem = str(filename.parent / filename.stem)
    input_file_type = filename.suffix

    if output_files["hvm"] is None:
        output_files["hvm"] = stem + ".hvm"
    if output_files["hco"] is None:
        output_files["hco"] = stem + ".hco"
    if output_files["htm"] is None:
        output_files["htm"] = stem + ".htm"
    if output_files["hvb"] is None:
        output_files["hvb"] = stem + ".hvb"
    if output_files["png"] is None:
        output_files["png"] = stem + ".png"
    if output_files["png"] is not None and output_files["gv"] is None:
        output_files["gv"] = stem + ".gv"

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
        code, scope = handle_hny(ns, output_files, parse_code_only, str(filename))
        if charm_flag:
            handle_hvm(ns, output_files, parse_code_only, code, scope)
            handle_hco(ns, output_files)
        else:
            print("Skipping Phases 2-5...", flush=True)
            legacy_harmony.dumpCode(print_code, code, scope)

    if input_file_type == ".hvm":
        print("Skipping Phase 1...", flush=True)
        handle_hvm(ns, output_files, parse_code_only, None, None)
        handle_hco(ns, output_files)
        
    if input_file_type == ".hco":
        print("Skipping Phases 1-4...", flush=True)
        handle_hco(ns, output_files)
