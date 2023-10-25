#!/usr/bin/env bash

echo "============================ PIPE ============================"

# piping commands: ;, &&, ||, &
echo -n "command1 ;  " ; echo "command2"
echo -n "command1 && " && echo "command2" # executed if command1 is successful
echo    "command1 || " || echo "command2" # executed if command1 is faild
echo $(sleep 0.1; echo "command1") & echo -n "command2 &  " # command1 is background shell task
sleep 0.2

# piping streams: |, <, <<, <<<, < <, >, >>, tee, xargs
# https://askubuntu.com/questions/678915/whats-the-difference-between-and-in-bash
# |      - redirect from stdout to stdin
# tee    - duplicate stdout to file
# xargs  - redirect from stdin to command arguments 
# >      - create empty file and write stdout to file
# >>     - write stdout to file
# <      - read from file to stdin
# << EOF - `here-document` read text block to stdin
# <<<    - `here-string` read string to stdin
# < <    - 'Process Substitution' 

# 0 /dev/stdin
# 1 /dev/stdout
# 2 /dev/stderr
#   /dev/null

echo hello > /dev/stdout
echo world > /dev/stderr
