#!/usr/bin/env bash

echo "============================ PIPE ============================"

# piping commands: ;, &&, ||, &
echo -n "command1 ;  " ; echo "command2"
echo -n "command1 && " && echo "command2" # executed if command1 is successful
echo    "command1 || " || echo "command2" # executed if command1 is faild
echo $(sleep 0.1; echo "command1") & echo -n "command2 &  " # command1 is background shell task
sleep 0.2

# piping streams: |, <, <<, >, >>