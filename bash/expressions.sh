#!/usr/bin/env bash

echo "============================ Math Expressions ============================"

echo $((10+5))
echo $(( (10+5)%10 ))

i=1
echo "i=$i"
(( i += 1 ))
(( i <<= 2 ))
echo "i=$i"
