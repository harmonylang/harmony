import setuptools
from setuptools.command.install import install
from setuptools.command.build_py import build_py

PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = "0.0.19a7"

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        super().run()

class BuildPythonCommand(build_py):
    def run(self):
        super().run()

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
            "modules/*.hny",
            "code/*.hny"
        ]
    },
    python_requires=">=3.6",
    cmdclass={
        "install": PostInstallCommand,
        "build_py": BuildPythonCommand
    }
)
