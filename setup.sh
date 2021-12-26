#/usr/bin/env sh

PACKAGE_DIR=harmony_model_checker
rm -rf build
rm -rf "$PACKAGE_DIR.egg-info"
rm -f "$PACKAGE_DIR/charm.exe"

python setup.py sdist bdist_wheel
