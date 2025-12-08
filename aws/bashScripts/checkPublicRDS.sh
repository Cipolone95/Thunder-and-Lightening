#!/bin/bash

# Check for required argument
if [ -z "$1" ]; then
  echo "Usage: $0 /path/to/directory"
  exit 1
fi

# Assign input path to variable
target_dir="$1"

# Make sure it's a valid directory
if [ ! -d "$target_dir" ]; then
  echo "Error: '$target_dir' is not a directory."
  exit 1
fi

# Initialize array
dir_list=()
for entry in "$target_dir"/*/ ; do
  # Remove trailing slash and path, keep just directory name
  dir_list+=("$(basename "${entry%/}")")
done

# Loop through and print each directory name
for dir in "${dir_list[@]}"; do
  #echo "====Checking Public RDS Instances AWS Account $dir====="
  output=$(tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws*.js| jq '.' | jq '.services.rds.findings | select(."rds-instance-publicly-accessible".flagged_items > 0) | { PubliclyAccessibleInstances: ."rds-instance-publicly-accessible".flagged_items }')
  if [[ -n "$output" ]]; then
    echo "====Publically Accessible RDS instance in AWS Account $dir====="
    echo
  fi
done
