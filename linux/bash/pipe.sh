#!/usr/bin/env bash

echo "============================ PIPE ============================"

# piping commands: ;, &&, ||, &
echo -n "command1 ;  " ; echo "command2"
echo -n "command1 && " && echo "command2" # executed if command1 is successful
echo    "command1 || " || echo "command2" # executed if command1 is faild
echo $(sleep 0.1; echo "command1") & echo -n "command2 &  " # command1 is background shell task
sleep 0.2

# piping streams: |, <, <<, >, >>, tee, xargs

# |     - redirect from stdout to stdin
# tee   - duplicate stdout to file
# xargs - redirect from stdin to command arguments 
# >     - create file and add to file
# >>    - add to file
# <     - ?
# <<    - ?
# <<<   - ?

# 0 /dev/stdin
# 1 /dev/stdout
# 2 /dev/stderr
#   /dev/null

echo hello > /dev/stdout
echo world > /dev/stderr
