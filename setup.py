from distutils import log
import setuptools
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

from pathlib import Path
import shutil
import subprocess

PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = "0.0.20a23"

PACKAGE_CONFIG = Path.home() / ".harmony-model-checker"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        if not PACKAGE_CONFIG.exists():
            PACKAGE_CONFIG.mkdir()
        super().run()

        # harmony_cmd = shutil.which("harmony")
        # if harmony_cmd is not None:
        #     ec = subprocess.run([harmony_cmd, "--build-model-checker"])
        # if harmony_cmd is None or ec != 0:
        #     super().announce(
        #         "Cannot build model checker automatically from setup. Please run [harmony --build-model-checker] after installation.",
        #         level=log.WARN
        #     )

class CustomBuildExt(build_ext):
    def build_extensions(self) -> None:
        self.compiler.set_executable("compiler_so", "gcc")
        self.compiler.set_executable("compiler_cxx", "gcc")
        self.compiler.set_executable("linker_so", "gcc")
        super().build_extensions()


module = Extension(
    f"{PACKAGE_NAME}.charm",
    sources=[f"{PACKAGE_NAME}/charm.c"],
    extra_compile_args=["-O3", "-std=c99", "-DNDEBUG", "-m64",
    # "-o", f"{PACKAGE_NAME}/charm.exe",
    "-lpthread"],
)

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
        "install": PostInstallCommand
    }
)
