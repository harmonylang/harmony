"""Describes how a Harmony run was produced, from the "config" object
and the per-module source hashes that the compiler records in the .hvm
file (and that the model checker copies into the .hco file)."""

import os

def source_name(mod):
    """How to show the file of a module: library modules by their name
    within Harmony, rather than where Harmony happens to be installed."""
    if mod.get("library"):
        return "<harmony>/" + os.path.basename(mod["file"])
    return mod["file"]

def run_info(hvm, top=None):
    """Returns a list of (label, value) pairs, where value is either a
    string or a list of strings.  Returns [] for files made by older
    versions of Harmony, which did not record this information."""
    config = hvm.get("config")
    if not config:
        return []
    info = [
        ("Program", config.get("input", "")),
        ("Command", config.get("command", "")),
        ("Harmony version", config.get("harmony_version", "")),
        ("Created", config.get("created", "")),
    ]
    if config.get("modules"):
        info.append(("Module substitutions",
            ", ".join(f"{k}={v}" for k, v in config["modules"].items())))
    if config.get("constants"):
        info.append(("Constants",
            ", ".join(f"{k}={v}" for k, v in config["constants"].items())))
    if config.get("interface"):
        info.append(("Interface", config["interface"]))
    if config.get("behavior"):
        text = config["behavior"]
        origin = config.get("behavior_origin")
        if origin and "command" in origin:
            text += " (made by: %s"%origin["command"]
            if "created" in origin:
                text += ", on %s"%origin["created"]
            text += ")"
        info.append(("Checked against behavior", text))
    # The model checker records its own options in the .hco file.  The
    # behavior file is reported above, by the name the user gave.
    options = [ o for o in (top or {}).get("checker_options", [])
                    if not o.startswith("-B") ]
    if options:
        info.append(("Checker options", " ".join(options)))
    sources = [ f"{name}: {source_name(mod)} (sha256 {mod['sha256'][:12]})"
                for name, mod in sorted(hvm.get("modules", {}).items())
                if "sha256" in mod ]
    if sources:
        info.append(("Sources", sources))
    return info

def run_info_comment(config, prefix):
    """The same information as comment lines, for the .tla and .tex
    outputs (which are produced before there is an .hvm file)."""
    lines = []
    for label, value in run_info({ "config": config }):
        if isinstance(value, list):
            value = ", ".join(value)
        lines.append(f"{prefix} {label}: {value}")
    return "\n".join(lines) + "\n" if lines else ""
