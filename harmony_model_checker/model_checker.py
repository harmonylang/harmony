import os
from harmony_model_checker.harmony import version
from pathlib import Path
import platform

CHARM_EXECUTABLE_FILE = Path(__file__).parent / "charm.exe"
CHARM_SOURCE_FILE = Path(__file__).parent / "charm.c"
BUILD_VERSION_FILE = Path(__file__).parent / "package_buildversion"

_INSTALLED_PACKAGE_VERSION = '.'.join(map(str, version))
def check_charm_model_checker_status_is_ok():
    if CHARM_EXECUTABLE_FILE.exists() and BUILD_VERSION_FILE.exists():
        with BUILD_VERSION_FILE.open("r") as f:
            current_version = f.read()
            if current_version == _INSTALLED_PACKAGE_VERSION:
                # Matches currently installed version, continue.
                return
    print("Model checker is not detected or may be out of sync with the model checker currently installed")
    print("Compiling model checker...")
    _build_model_checker()
    if not CHARM_EXECUTABLE_FILE.exists():
        print("Failed to compile the model checker (using gcc).")
        return False
    with BUILD_VERSION_FILE.open("w") as f:
        f.write(_INSTALLED_PACKAGE_VERSION)
    print("Successfully compiled the model checker (using gcc).")
    return True

def _build_model_checker():
    ec = os.system(f"gcc -O3 -std=c99 -DNDEBUG {CHARM_SOURCE_FILE} -m64 -o {CHARM_EXECUTABLE_FILE} -lpthread")
    if ec != 0 or not CHARM_EXECUTABLE_FILE.exists():
        exe = Path(__file__).parent / ("charm." + platform.system() + ".exe")
        if exe.exists():
            ec = os.system(f"{exe} -x")
            if ec == 0:
                exe.rename(CHARM_EXECUTABLE_FILE)
