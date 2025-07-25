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
  #echo "====$dir====="
  #output=$(tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws-AWSReadOnlyAccess-$dir.js| jq '.' | jq '.services.iam.credential_reports.[] | select((.access_key_1_last_used_date != null and .access_key_1_last_used_date < "2025") or (.access_key_2_last_used_date != null and .access_key_2_last_used_date < "2025")) | { ARN: .arn, K1_Active: .access_key_1_active, Last_Used_K1: .access_key_1_last_used_date, K2_Active: .access_key_2_active, Last_Used_K2: .access_key_2_last_used_date}')
  output=$(tail -n +2 $target_dir/$dir/scoutsuite-results/scoutsuite_results_aws-AWSReadOnlyAccess-$dir.js| jq '.' | jq --argjson cutoff "$(date -d '90 days ago' +%s)" '
.services.iam.credential_reports[]
| select(
    (.access_key_1_last_used_date != null and (try ( .access_key_1_last_used_date | fromdateiso8601 ) catch 0) < $cutoff)
    or
    (.access_key_2_last_used_date != null and (try ( .access_key_2_last_used_date | fromdateiso8601 ) catch 0) < $cutoff)
  )
| {
    ARN: .arn,
    K1_Active: .access_key_1_active,
    Last_Used_K1: .access_key_1_last_used_date,
    K2_Active: .access_key_2_active,
    Last_Used_K2: .access_key_2_last_used_date
}')
  if [[ -n "$output" ]]; then
    echo $output | jq
    echo
  fi
done
