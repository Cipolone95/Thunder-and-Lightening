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
  echo "====Checking Buckets from GCP Project $dir====="

    tail -n +2 scoutReports/$dir/scoutsuite-results/scoutsuite_results_$dir.js | jq '.' | jq '
if (
  .services.cloudstorage.findings."cloudstorage-bucket-no-public-access-prevention".flagged_items > 0 or
  .services.cloudstorage.findings."cloudstorage-bucket-allAuthenticatedUsers".flagged_items > 0 or
  .services.cloudstorage.findings."cloudstorage-bucket-allUsers".flagged_items > 0
)
then "Buckets Insecure"
else "Buckets Secure"
end'


done