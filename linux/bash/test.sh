#!/usr/bin/env bash

echo "============================ Test ============================"
# `test` == `[` ~= `[[`

test_var="true"
if [[ "$test_var" == "true" ]]
then
    echo "test_var is true"
else
    echo "test_var is something else"
fi

test_var=""
if [[ "$test_var" == "true" ]]; then
    echo "test_var is true"
else
    echo "test_var is something else"
fi

test_var="true"
if [ "$test_var" == "true" ]; then
    echo "test_var is true"
else
    echo "test_var is something else"
fi

# Regexp
email=me@example.com
if [[ "$email" =~ [a-z]+@[a-z]{2,}\.(com|net|org) ]]
then
    echo "Valid email!"
else
    echo "Invalid email!"
fi

if grep $(whoami) /etc/passwd
then
    echo "i'm registered in the system"
fi