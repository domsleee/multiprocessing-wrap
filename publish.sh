#!/bin/bash
if [[ $# != 1 || ( $1 != "prod" && $1 != "test" ) ]]; then
  echo "usage: $0 prod"
  echo "       $0 test"
  exit 1
fi
rm -rf dist/
python3 setup.py bdist_wheel sdist

if [[ $1 == "prod" ]]; then
  twine upload dist/*
else
  twine upload --repository-url https://test.pypi.org/legacy/ dist/*
fi