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
from harmony_model_checker.exception import HarmonyCompilerError, HarmonyCompilerErrorCollection
import harmony_model_checker.harmony.harmony as legacy_harmony
from harmony_model_checker.harmony.genhtml import GenHTML
from harmony_model_checker.harmony.brief import Brief
from harmony_model_checker.compile import do_compile


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
args.add_argument("--module", "-m", action="append", type=str,
                  metavar="module=version", help="select a module version")
args.add_argument("-i", "--intf", type=str, metavar="expr",
                  help="specify in interface function")
args.add_argument("-s", action="store_true",
                  help="silent (do not print periodic status updates)")
args.add_argument("-v", "--version", action="store_true",
                  help="print version number")
args.add_argument("-o", action='append', type=pathlib.Path,
                  help="specify output file (.hvm, .hco, .hfa, .htm. .tla, .png, .gv)")
args.add_argument("-j", action="store_true",
                  help="list machine code in JSON format")
args.add_argument("--noweb", action="store_true", default=False,
                  help="do not automatically open web browser")
args.add_argument("--suppress", action="store_true",
                  help="generate less terminal output")

# Internal flags
args.add_argument("--cf", action="append", type=str, help=argparse.SUPPRESS)

args.add_argument("files", metavar="harmony-file",
                  type=pathlib.Path, nargs='*', help="files to compile")


def main():
    ns = args.parse_args()

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
            with open(output_files["hvm"], "w", encoding='utf-8') as fp:
                json.dump(data, fp)
        else:
            for e in errors:
                print(f"Line {e.line}:{e.column} at {e.filename}, {e.message}")
                print()
        return 1

    if parse_code_only:
        with open(output_files["hvm"], "w", encoding='utf-8') as f:
            f.write(json.dumps({"status": "ok"}))
        return

    if output_files["tla"] is not None:
        with open(output_files["tla"], "w", encoding='utf-8') as f:
            legacy_harmony.tla_translate(f, code, scope)

    # Analyze liveness of variables
    if charm_flag:
        # see if there is a configuration file
        with open(output_files["hvm"], "w", encoding='utf-8') as fd:
            legacy_harmony.dumpCode("json", code, scope, f=fd)

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
    else:
        legacy_harmony.dumpCode(print_code, code, scope)
