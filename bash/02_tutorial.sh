#!/bin/bash

my_first_function () 
{
  # amount of possible arguments
  echo "Max arguments: $(getconf ARG_MAX)"
  
  # chmod +x ./01_titorial.sh
  
  echo "Я, $(whoami) нахожусь здесь: $(pwd)"
  echo "Home dir: $HOME"
  
  my_var=42
  my_name="Daniil"
  echo "$my_name and $my_var"
  
  echo "math = $(( my_var / 2))"
  
  if grep $(whoami) /etc/passwd
  then
    echo "i'm registered in the system"
  fi
  
  echo $((42>10)) or $((42<10))
  
  # IFS - Internal Field Separator
  # IFS=$'\n'
  # or 
  # IFS=:
  
  for file in $HOME/Documents/* ; do
      if [ -d "$file" ]
      then 
        echo "DIRECORY: $file"
      elif [ -f "$file" ]
      then 
        echo "FILE: $file"
      fi
  done

}

my_first_function

# read -s -p "Enter some password: " pass
# echo -e "\nhaaa, catch u: $pass"

echo "pattern1pattern2pattern3" | sed 's/pattern1/XXX/' | sed 's/pattern3/YYY/'

