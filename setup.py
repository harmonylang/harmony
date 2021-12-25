import os

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess

PACKAGE_NAME = 'harmony_model_checker'

# Source: https://stackoverflow.com/questions/33168482/compiling-installing-c-executable-using-pythons-setuptools-setup-py
def compile_and_install_software():
    """
    Used the subprocess module to compile/install the C software.
    """
    src_path = PACKAGE_NAME

    # compile the software
    result = subprocess.call([
        "gcc", "-g", "-std=c99", "charm.c",
        "-m64", "-o", "charm.exe", "-lpthread"
    ], cwd=src_path, shell=True)
    if result == 0:
        print("Successfully compiled model checker")
    else:
        print("Failed to compile model checker")


class PostDevelopCommand(develop):
    """
    Post-installation for development mode.
    """
    def run(self):
        compile_and_install_software()
        super().run()


class PostInstallCommand(install):
    def run(self):
        compile_and_install_software()
        super().run()


setuptools.setup(
    name=PACKAGE_NAME,
    version="0.0.5",
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
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
)
