#!/bin/bash

ERRORS=0
# pylint --rcfile="test/.pylintrc" test || ERRORS=1

if [ "$ERRORS" -eq 0 ]; then
	python3.5 test/testrunner.py
fi