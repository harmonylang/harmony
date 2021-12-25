#/usr/bin/env sh

PACKAGE_DIR=harmony_model_checker

turn_into_package() {
    touch "$1/__init__.py"
}

rm -rf "$PACKAGE_DIR.egg-info"

turn_into_package "$PACKAGE_DIR/code"
turn_into_package "$PACKAGE_DIR/modules"

# harmony and harmony.bat do not need to be copied
# as pip creates a console script when the package is installed.

python setup.py sdist bdist_wheel
