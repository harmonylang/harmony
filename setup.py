import distutils.errors
from typing import List, NamedTuple
import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext


PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = "0.0.22a9"

class CompilerArgs(NamedTuple):
    name: str
    compile_args: List[str]
    linker_args: List[str]

compiler_and_args = [
    CompilerArgs(
        "gcc",
        ["-pthread", "-m64", "-O3", "-fPIC"],
        "-pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2".split(" ")
    ),
    CompilerArgs(
        "cc",
        ["-pthread", "-m64", "-O3", "-fPIC"],
        "-pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2".split(" ")
    ),
    CompilerArgs(
        "clang",
        ["-pthread", "-m64", "-O3", "-fPIC"],
        "-pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -Wl,-Bsymbolic-functions -Wl,-z,relro -g -fwrapv -O2 -g -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2".split(" ")
    )
]

# try:
#     from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
#     class bdist_wheel(_bdist_wheel):
#         def finalize_options(self):
#             _bdist_wheel.finalize_options(self)
#             # Mark us as not a pure python package
#             self.root_is_pure = False
#         def get_tag(self):
#             python, abi, plat = _bdist_wheel.get_tag(self)
#             print("Getting tags", python, abi, plat)
#             # We don't contain any python source
#             python, abi = 'py2.py3', 'none'
#             return python, abi, plat
# except ImportError:
#     bdist_wheel = None

class BuildExtCommand(build_ext):
    def build_extension(self, ext) -> None:
        try:
            # Try to build the extension with default OS build tools.
            super().build_extension(ext)
            return
        except (distutils.errors.DistutilsPlatformError, distutils.errors.CompileError) as e:
            print("Encountered error when building by default configurations")

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
                pass
        if encountered_error is not None:
            raise encountered_error


module = Extension(f"{PACKAGE_NAME}.charm", sources=[f"{PACKAGE_NAME}/charm.c"])

setuptools.setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    author="Robbert van Renesse",
    author_email="rvr@cs.cornell.edu",
    description="Harmony Programming Language",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy; python_version >= "1.21"',
        'matplotlib; python_version >= "3.5"',
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
            "modules/*.hny",
            "code/*.hny"
        ]
    },
    python_requires=">=3.6",
    ext_modules=[module],
    cmdclass={
        "build_ext": BuildExtCommand,
        # "bdist_wheel": bdist_wheel,
    }
)
