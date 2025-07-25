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
  #echo "====Checking S3 Bucket Permissions AWS Account $dir====="
  echo $dir
  tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws*.js| jq '.' | jq '.services.s3.buckets[] 
  | select(
      .public_access_block_configuration.BlockPublicAcls != true 
      or .public_access_block_configuration.BlockPublicPolicy != true 
      or .public_access_block_configuration.IgnorePublicAcls != true 
      or .public_access_block_configuration.RestrictPublicBuckets != true
    ) 
  | .arn' | sed 's/"//g'


done
