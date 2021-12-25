#/usr/bin/env sh

PACKAGE_DIR=harmony_model_checker

turn_into_package() {
    touch "$1/__init__.py"
}

rm -rf "$PACKAGE_DIR.egg-info"

cp -r code/ "$PACKAGE_DIR"

turn_into_package "$PACKAGE_DIR/code"
turn_into_package "$PACKAGE_DIR/modules"

# Copy relevant files into published package directory
cp iface.py dfacmp.py charm.Windows.exe "$PACKAGE_DIR"

# harmony and harmony.bat do not need to be copied
# as pip creates a console script when the package is installed.

python setup.py install

rm -rf "$PACKAGE_DIR.egg-info"
