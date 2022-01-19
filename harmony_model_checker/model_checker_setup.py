import os
from pathlib import Path
import platform

PACKAGE_CONFIG_PATH = Path.home() / ".harmony-model-checker"
PACKAGE_INSTALL_PATH = Path(__file__).parent

CHARM_SOURCE_FILE = PACKAGE_INSTALL_PATH / "charm.c"
CHARM_EXECUTABLE_FILE = PACKAGE_CONFIG_PATH / "charm.exe"

def check_charm_model_checker_status_is_ok():
    if CHARM_EXECUTABLE_FILE.exists():
        return True
    # Compile the model checker otherwise
    print("#" * 60)
    print("Model checker is not detected or may be out of sync with the model checker currently installed")
    success = build_model_checker()
    if success:
        print("Successfully compiled the model checker (using gcc).")
    else:
        print("Failed to compile the model checker (using gcc).")

    print("#" * 60 + '\n')  # extra newline to separate build-process from model-checker
    return success

_C_COMPILERS = ["gcc", "clang", "cc"]
def build_model_checker():
    if not PACKAGE_CONFIG_PATH.exists():
        PACKAGE_CONFIG_PATH.mkdir()

    print("Compiling model checker...")
    ec = 1
    for compiler in _C_COMPILERS:
        ec = os.system(f"{compiler} -O3 -std=c99 -DNDEBUG {CHARM_SOURCE_FILE} -m64 -o {CHARM_EXECUTABLE_FILE} -lpthread")
        if ec == 0:
            break

    if ec != 0 or not CHARM_EXECUTABLE_FILE.exists():
        exe = Path(__file__).parent / ("charm." + platform.system() + ".exe")
        if exe.exists():
            ec = os.system(f"{exe} -x")
            if ec == 0:
                exe.rename(CHARM_EXECUTABLE_FILE)
    return CHARM_EXECUTABLE_FILE.exists()
