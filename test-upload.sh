#!/usr/bin/env sh

rm -rf dist/

./setup.sh

twine upload --repository-url https://test.pypi.org/legacy/ dist/*
