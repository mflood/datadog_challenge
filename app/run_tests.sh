#!/bin/sh

COVERAGE_ARG=$1
DO_COVERAGE=no
if [ "$COVERAGE_ARG" != "" ]; then
    if [ "$COVERAGE_ARG" == "coverage" ]; then
        DO_COVERAGE=yes
    else
        echo "Usage: $0 [coverage"]
        exit 1
    fi
fi

source venv/bin/activate

if [ "$DO_COVERAGE" == "yes" ];then
    coverage run --source datadog -m pytest
    coverage report -m
else
    #pytest -vv

    # use these args if you want to see logging output
    pytest -vv --log-cli-level 1 tests
fi
