#!/usr/bin/env bash

echo "============================ Variables ============================"

var="var_value"
echo "---------"

echo $var
echo "$var"
echo '$var'
echo "${var}"
echo "---------"

echo "${var:-"default"}"
echo "${var2:-"default"}"
echo "sort of sed for variables: ${var/v/V}"
echo "---------"

echo "length of var: ${#var}"
echo "symbols from 3 to 3+6 of var: ${var:3:6}"
echo "symbols from 3 to end of var: ${var:3}"
echo "symbols from end-6 to end of var: ${var: -6}"
echo "---------"

other_variable="var"
echo "${other_variable} is ${!other_variable}"
echo "---------"

# Built-in variables
echo "Last program's return value: $?"
echo "Script's PID: $$"
echo "Number of arguments passed to script: $#"
echo "All arguments passed to script: $@"
echo "Script's arguments separated into different variables: $1 $2..."
echo "---------"
echo "pwd command: $(pwd)"
echo "PWD var: $PWD"
echo "---------"
echo "Home for $USER is $HOME"