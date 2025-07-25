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
  #echo "====Checking SNS in AWS Account $dir====="
  output=$(tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws-AWSReadOnlyAccess-$dir.js| jq '.' | jq '.services.iam.findings."iam-root-account-no-mfa" | select(.flagged_items | length > 0)')
  if [[ -n "$output" ]]; then
    echo "====Root MFA is not enabled in AWS Account $dir====="
    echo
  fi

done
