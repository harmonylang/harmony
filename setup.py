from pathlib import Path
import setuptools
from setuptools.command.install import install
from setuptools.command.build_py import build_py
import os

PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = "0.0.19a4"

def compile():
    os.system(f"gcc -O3 -std=c99 -DNDEBUG harmony_model_checker/charm.c -m64 -o harmony_model_checker/charm.exe -lpthread")

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        super().run()

class BuildPythonCommand(build_py):
    def run(self):
        compile()
        super().run()

# try:
#     from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
#     class bdist_wheel(_bdist_wheel):
#         def run(self):
#             print("Running bdist wheel command")
#             compile()
#             super().run()
# except ImportError:
#     bdist_wheel = None


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
        'automata-lib; python_version >= "5.0"'
    ],
    include_package_data=True,
    package_data={
        PACKAGE_NAME: [
            "charm.c",
            "charm.Windows.exe",
            "charm.exe",
            "modules/*.hny",
            "code/*.hny"
        ]
    },
    python_requires=">=3.6",
    cmdclass={ "install": PostInstallCommand, "build_py": BuildPythonCommand }
)
