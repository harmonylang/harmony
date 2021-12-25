#/usr/bin/env sh

PACKAGE_DIR=harmony_model_checker

turn_into_package() {
    touch "$1/__init__.py"
}

rm -rf "$PACKAGE_DIR.egg-info"

cp -r code/ "$PACKAGE_DIR"
cp -r modules/ "$PACKAGE_DIR"

turn_into_package "$PACKAGE_DIR/code"
turn_into_package "$PACKAGE_DIR/modules"

python setup.py install

rm -rf "$PACKAGE_DIR.egg-info"
