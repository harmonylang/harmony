import os
import subprocess
from pathlib import Path
import platform

CHARM_EXECUTABLE_FILE = Path(__file__).parent / "charm.exe"
CHARM_SOURCE_FILE = Path(__file__).parent / "charm.c"


def build_model_checker():
    ec = subprocess.call([
        "gcc", "-O3", "-std=c99", "-DNDEBUG", str(CHARM_SOURCE_FILE),
        "-m64", "-o", str(CHARM_EXECUTABLE_FILE), "-lpthread"
    ])
    if ec != 0 or not CHARM_EXECUTABLE_FILE.exists():
        exe = Path(__file__).parent / ("charm." + platform.system() + ".exe")
        if exe.exists():
            ec = subprocess.call([str(exe), "-x"])
            if ec == 0:
                exe.rename(CHARM_EXECUTABLE_FILE)
