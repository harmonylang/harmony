import os
import subprocess
from pathlib import Path
import platform

CHARM_EXECUTABLE_FILE = Path(__file__).parent / "charm.exe"


def build_model_checker():
    ec = subprocess.call(
        ["gcc", "-O3", "-std=c99", "-DNDEBUG", "charm.c", "-m64", "-o", str(CHARM_EXECUTABLE_FILE)])
    if ec != 0 or not CHARM_EXECUTABLE_FILE.exists():
        exe = Path(__file__).parent / ("charm." + platform.system() + ".exe")
        if exe.exists():
            ec = subprocess.call([str(exe), "-x"])
            if ec == 0:
                exe.rename(CHARM_EXECUTABLE_FILE)
