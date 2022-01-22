import sys
import os
import platform


def general_build(py_cmds):
    for p in py_cmds:
        os.system(f"{p} -m pip install wheel")
        os.system(f"{p} setup.py bdist_wheel")

def build_darwin():
    py_cmds = ["python3.6", "python3.7", "python3.8", "python3.9", "python3.10"]
    general_build(py_cmds)

def build_linux():
    py_cmds = ["python3.6", "python3.7", "python3.8", "python3.9", "python3.10"]
    general_build(py_cmds)


def build_windows():
    py_cmds = ["py -3.6", "py -3.7", "py -3.8", "py -3.9", "py -3.10"]
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

