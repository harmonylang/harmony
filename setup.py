import os
import os.path
from pathlib import Path
import pathlib
from typing import List, NamedTuple

import setuptools
import distutils.errors
from setuptools import Extension
from setuptools.command.build_ext import build_ext


# Checks the version number of package in the same way as pip.
def read(rel_path: str) -> str:
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with open(os.path.join(here, rel_path), encoding='utf-8') as fp:
        return fp.read()

def get_version(rel_path: str) -> str:
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")

PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = get_version(f"{PACKAGE_NAME}/__init__.py")

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


class CompilerArgs(NamedTuple):
    name: str
    compile_args: List[str]
    linker_args: List[str]


EXTRA_COMPILE_ARGS = ["-pthread", "-m64", "-O3", "-DNDEBUG", "-fPIC"] # the -fPIC flag is required to create a shared object file.

# Extra link args used by gcc in Linux.
# Tested flags with cc and clang
EXTRA_LINK_ARGS = ['-pthread', '-shared', '-Wl,-O1', '-Wl,-Bsymbolic-functions', '-Wl,-Bsymbolic-functions', '-Wl,-z,relro', '-g', '-fwrapv', '-O2', '-Wl,-Bsymbolic-functions',
                   '-Wl,-z,relro', '-g', '-fwrapv', '-O2', '-g', '-fstack-protector-strong', '-Wformat', '-Werror=format-security', '-Wdate-time', '-D_FORTIFY_SOURCE=2']

compiler_and_args = [
    CompilerArgs(
        "gcc",
        EXTRA_COMPILE_ARGS,
        EXTRA_LINK_ARGS
    ),
    CompilerArgs(
        "cc",
        EXTRA_COMPILE_ARGS,
        EXTRA_LINK_ARGS
    ),
    CompilerArgs(
        "clang",
        EXTRA_COMPILE_ARGS,
        EXTRA_LINK_ARGS
    )
]


class BuildExtCommand(build_ext):
    def build_extension(self, ext) -> None:
        try:
            # Try to build the extension with the default OS build tools.
            super().build_extension(ext)
            return
        except (distutils.errors.DistutilsPlatformError, distutils.errors.CompileError) as e:
            print("Encountered error when building by default configurations")
            print("Buidling with backup configurations")

        encountered_error = None
        for c in compiler_and_args:
            ext.extra_compile_args = c.compile_args
            ext.extra_link_args = c.linker_args
            name = c.name
            self.compiler.set_executable("linker_so", name)
            self.compiler.set_executable("compiler_so", name)
            self.compiler.set_executable("compiler_cxx", name)
            try:
                super().build_extension(ext)
                return
            except distutils.errors.CompileError as e:
                encountered_error = e

        if encountered_error is not None:
            raise encountered_error


CHARM_PKG_PATH = pathlib.Path(PACKAGE_NAME) / "charm"
def get_c_extension_src():
    sources = []
    base_dir = CHARM_PKG_PATH
    D = [base_dir, base_dir / "iface", base_dir / "python_ext"]
    for d in D:
        sources.extend([str(f) for f in d.glob('*.c')])
    return sources

def get_c_extension_include_dirs():
    return [
        str(CHARM_PKG_PATH),
        str(CHARM_PKG_PATH / 'iface'),
        str(CHARM_PKG_PATH / 'python_ext'),
    ]


module = Extension(
    f"{PACKAGE_NAME}.charm",
    sources=get_c_extension_src(),
    include_dirs=get_c_extension_include_dirs()
)

setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="Robbert van Renesse",
    author_email="rvr@cs.cornell.edu",
    description="Harmony Programming Language",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'antlr-denter; python_version >= "1.3.1"',
        'antlr4-python3-runtime; python_version == "4.9.3"',
        'automata-lib',
        'pydot',
        'requests',
    ],
    license="BSD",
    url="https://harmony.cs.cornell.edu",
    include_package_data=True,
    package_data={
        PACKAGE_NAME: [
            "charm.c",
            "modules/*.hny",
            "harmony/charm.js",
            "harmony/charm.css"
        ]
    },
    entry_points={
        'console_scripts': [
            'harmony=harmony_model_checker.main:main',
            'iface=harmony_model_checker.iface:main'
        ]
    },
    python_requires=">=3.6",
    ext_modules=[module],
    cmdclass={
        "build_ext": BuildExtCommand
    }
)
