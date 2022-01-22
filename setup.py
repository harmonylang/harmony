import distutils.errors
from typing import List, NamedTuple
import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from pathlib import Path


PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = "0.0.23"

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


class CompilerArgs(NamedTuple):
    name: str
    compile_args: List[str]
    linker_args: List[str]


EXTRA_COMPILE_ARGS = ["-pthread", "-m64", "-O3", "-DNDEBUG", "-fPIC"]

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


module = Extension(
    f"{PACKAGE_NAME}.charm",
    sources=[f"{PACKAGE_NAME}/charm.c"]
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
        'automata-lib; python_version >= "5.0"',
        'pydot; python_version == "1.4.2"'
    ],
    include_package_data=True,
    package_data={
        PACKAGE_NAME: [
            "charm.c",
            "charm.Windows.exe",
            "modules/*.hny"
        ]
    },
    python_requires=">=3.6",
    ext_modules=[module],
    cmdclass={
        "build_ext": BuildExtCommand
    }
)
