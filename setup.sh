#/usr/bin/env sh

PACKAGE_DIR=harmony_model_checker
rm -rf "$PACKAGE_DIR.egg-info"

python setup.py sdist bdist_wheel
