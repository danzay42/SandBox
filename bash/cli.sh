#!/usr/bin/env bash

echo "============================ CLI ============================"

read var
echo "You set var = $var"

# Case
case "$var" in
    # List patterns for the conditions you want to meet
    0) echo "There is a zero.";;
    1) echo "There is a one.";;
    -h) echo "Help message";;
    *) echo "It is not null.";;  # match everything
esac
