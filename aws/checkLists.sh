#!/bin/bash

# Ensure a file is provided as the first argument
if [ $# -ne 1 ]; then
  echo "Usage: $0 <list1_file>"
  exit 1
fi

list1_file=$1

# Check if the file exists
if [ ! -f "$list1_file" ]; then
  echo "Error: File '$list1_file' not found!"
  exit 1
fi

# Get the output of ls (list 2)
list2=$(ls )

# Loop through each line in list1_file
while IFS= read -r number; do
  # Check if the number is not in list2
  if [[ ! "$list2" =~ (^|[[:space:]])"$number"($|[[:space:]]) ]]; then
    echo "$number"
  fi
done < "$list1_file"
