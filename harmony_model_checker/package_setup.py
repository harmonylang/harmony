import os
from pathlib import Path
import platform

PACKAGE_CONFIG_PATH = Path.home() / ".harmony-model-checker"
PACKAGE_INSTALL_PATH = Path(__file__).parent

CHARM_SOURCE_FILE = PACKAGE_INSTALL_PATH / "charm.c"
CHARM_EXECUTABLE_FILE = PACKAGE_CONFIG_PATH / "charm.exe"

BUILD_VERSION_FILE = PACKAGE_CONFIG_PATH / "package_buildversion"
INSTALLED_BUILD_VERSION_FILE = PACKAGE_INSTALL_PATH / "package_buildversion"

def check_charm_model_checker_status_is_ok():
    if not PACKAGE_CONFIG_PATH.exists():
        PACKAGE_CONFIG_PATH.mkdir()
    with INSTALLED_BUILD_VERSION_FILE.open("r") as f:
        installed_version = f.read()

    if CHARM_EXECUTABLE_FILE.exists() and BUILD_VERSION_FILE.exists():
        with BUILD_VERSION_FILE.open("r") as f:
            current_version = f.read()
        if current_version == installed_version:
            # Matches currently installed version.
            return True
        # Compile the model checker otherwise

    success = _build_model_checker()
    if success:
        with BUILD_VERSION_FILE.open("w") as f:
            f.write(installed_version)
        print("Successfully compiled the model checker (using gcc).")
    else:
        print("Failed to compile the model checker (using gcc).")
    return success


def _build_model_checker():
    print("Model checker is not detected or may be out of sync with the model checker currently installed")
    print("Compiling model checker...")

    ec = os.system(f"gcc -O3 -std=c99 -DNDEBUG {CHARM_SOURCE_FILE} -m64 -o {CHARM_EXECUTABLE_FILE} -lpthread")
    if ec != 0 or not CHARM_EXECUTABLE_FILE.exists():
        exe = Path(__file__).parent / ("charm." + platform.system() + ".exe")
        if exe.exists():
            ec = os.system(f"{exe} -x")
            if ec == 0:
                exe.rename(CHARM_EXECUTABLE_FILE)
    return CHARM_EXECUTABLE_FILE.exists()
