#!/bin/bash

ERRORS=0
make lint || ERRORS=1

REPO=$1
VERSION=$2
PUSH=$3
UPLOAD=$4

if [ "$ERRORS" -eq 0 ]; then
	python lib.py setup.py $VERSION update > setup_tmp.py
	python lib.py lib.py $VERSION update > lib_tmp.py
	python lib.py README.md $VERSION update > README_tmp.md

	rm lib.py
	mv lib_tmp.py lib.py

	rm setup.py
	mv setup_tmp.py setup.py

	rm README.md
	mv README_tmp.md README.md

	if [ "$REPO" = "pypitest" ] || [ "$PUSH" = "true" ]; then
		git add .
		git commit -n -m "Release Version: $VERSION"
		git tag -a "v$VERSION" -m "Version: $VERSION"
		git push origin master --tags
	fi

	if [ "$UPLOAD" = "true" ]; then
		python setup.py sdist upload -r $REPO
	fi
fi