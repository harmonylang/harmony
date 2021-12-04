import os
from distutils.core import setup

requires = [
    "numpy",
    "matplotlib",
    "antlrdenter",
    "antlr4python3runtime",
    "automatalib"
]

modules_files = [os.path.join("modules", f) for f in os.listdir("modules")]
code_files = [os.path.join("code", f) for f in os.listdir("code")]

setup(
    name='harmony',
    version='1.2',
    url='https://harmony.cs.cornell.edu/',
    author='Robbert van Renesse',
    author_email='rvr@cs.cornell.edu',
    description='The Harmony programming language',
    long_description=open('README.txt').read(),
    requires=requires,
    packages=["harmony_lib"],
    data_files=[
        ("modules", modules_files),
        ("code", code_files)
    ]
)
