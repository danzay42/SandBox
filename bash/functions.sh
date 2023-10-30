#!/usr/bin/env bash

echo "============================ Functions ============================"

echo "Max arguments: $(getconf ARG_MAX)"

function foo ()
{
    echo "foo arguments: $@"
    echo "args by positions: $1 $2..."
    return 0
}
echo "run foo: $(foo abc cda)"

bar () {
    echo "bar arguments: $@"
    echo "args by positions: $1 $2..."
}
echo "run bar: $(bar hello world)"
