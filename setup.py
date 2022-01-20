from distutils import log
import setuptools
from setuptools import Extension
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext

from pathlib import Path

PACKAGE_NAME = 'harmony_model_checker'
PACKAGE_VERSION = "0.0.22a6"


module = Extension(
    f"{PACKAGE_NAME}.charm",
    sources=[f"{PACKAGE_NAME}/charm.c"],
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
)
