import sys
import os
import platform
from typing import Dict


def general_build(py_cmds: Dict[str, str]):
    successful_builds = []
    for (version, p) in py_cmds.items():
        if os.system(f"{p} -m pip install wheel") != 0:
            print(f"Failed to install wheel for Python version {version}.")
            print("Skipping build...")
            continue

        if os.system(f"{p} setup.py bdist_wheel") != 0:
            print(f"Failed to build wheel for Python version {version}.")
            continue

        successful_builds.append(version)
    
    if successful_builds:
        print(f"Successfully built wheels for versions [{', '.join(successful_builds)}].")
    else:
        print("No wheels were built.")


def build_darwin():
    py_cmds = {
        "3.6": "python3.6",
        "3.7": "python3.7",
        "3.8": "python3.8",
        "3.9": "python3.9",
        "3.10": "python3.10"
    }
    general_build(py_cmds)

def build_linux():
    py_cmds = {
        "3.6": "python3.6",
        "3.7": "python3.7",
        "3.8": "python3.8",
        "3.9": "python3.9",
        "3.10": "python3.10"
    }
    general_build(py_cmds)

def build_windows():
    py_cmds = {
        "3.6": "py -3.6",
        "3.7": "py -3.7",
        "3.8": "py -3.8",
        "3.9": "py -3.9",
        "3.10": "py -3.10"
    }
    general_build(py_cmds)


def main():
    system = platform.system()
    if system == "Windows":
        build_windows()
    elif system == "Linux":
        build_linux()
    elif system == "Darwin":
        build_darwin()
    else:
        print(f"Non-supported system {system}")


if __name__ == "__main__":
    sys.exit(main())

