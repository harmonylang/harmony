import os

import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install
import subprocess


def compile_charm():
    subprocess.call([
        "gcc", "-g", "-std=c99", "charm.c",
        "-m64", "-o", "charm.exe", "-lpthread"
    ])


class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        compile_charm()


class PostInstallCommand(install):
    def run(self):
        install.run(self)
        compile_charm()


setuptools.setup(
    name="harmony_model_checker",
    version="0.0.1",
    author="Robbert van Renesse",
    author_email="rvr@cs.cornell.edu",
    description="Harmony Programming Language",
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "numpy",
        "matplotlib",
        "antlr-denter",
        "antlr4-python3-runtime",
        "automata-lib"
    ],
    include_package_data=True,
    package_data={
        "modules": ["modules/*.hny"],
        "code": ["code/*.hny"],
        "": ["charm.c", "charm.Windows.exe"],
    },
    python_requires=">=3.6",
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand
    }
)
