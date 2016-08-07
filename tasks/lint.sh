#!/bin/bash

PLATFORM=`uname`
ERRORS=0

make lint || ERRORS=1

exit $ERRORS
