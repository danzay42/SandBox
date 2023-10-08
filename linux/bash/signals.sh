#!/usr/bin/env bash

# catch SIGNAL and execute command 
trap "command" SIGNAL
# Remove active traps 
trap - SIGNAL