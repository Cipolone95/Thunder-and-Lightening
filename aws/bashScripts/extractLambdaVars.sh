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
  echo "====Pulling Lambda Environment Variables from AWS Account $dir====="
  # tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws-$dir.js| jq '.' | jq '.services.awslambda.regions[].functions[] 
  #   | select(.env_variables != null and (.env_variables | to_entries | map(.key) | join(" ") | test("secret|password|api|key|auth|token"; "i")))
  #   | {arn: .arn, Environment: .env_variables}'

    # tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws-$dir.js| jq '.' | jq '.services.awslambda.regions[].functions[] 
    # | select(.env_variables != null and (.env_variables | length > 0)) 
    #    | select(.env_variables != null)
    #    | .env_variables
    #    | to_entries[]
    #    | "\(.key)=\(.value)"' | sed -E 's/^"?(.*?)"?$/\1/'
    tail -n +2 "$target_dir/$dir/scoutsuite-results/scoutsuite_results_aws-AWSReadOnlyAccess-$dir.js" \
| jq '.' \
| jq -r '.services.awslambda.regions[].functions[] 
    | select(.env_variables != null and (.env_variables | length > 0)) 
    | "\(.arn)\n" + 
      (.env_variables | to_entries[] | "\(.key)=\(.value)") + "\n"'
done
