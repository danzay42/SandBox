#!/usr/bin/env bash

echo "============================ Iterations ============================"

# Arrays
array=(one two three four five six)
echo "${array[@]}"
echo "first element of array: ${array} or ${array[0]}"
echo "length of array: ${#array[@]}"
echo "slice of array: ${array[@]:3:2}"
echo "---------"

# for loop
for i in ${array[@]}
do
    echo "array element is $i"
done

for ((i=1; i<3; i++)); do echo "traditional loop $i"; done

# while loop
while [ true ]
do
    echo "loop body here..."
    break
done
echo "---------"

# Built-in iterable
echo {-5..5}
echo {a..z}