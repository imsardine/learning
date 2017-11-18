#!/usr/bin/env bash
if [ $# -ne 1 ] ; then
    echo 'USAGE: docker run --rm custom-hello <WHO>'
    exit 1
else
    echo "Hello, $1"'!'
fi
