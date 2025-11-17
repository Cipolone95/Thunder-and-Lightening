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

echo "====Projects with Insequre Big Query Datasets====="

# Loop through and print each directory name
for dir in "${dir_list[@]}"; do
  #echo "====Checking Privileged Service Accounts from GCP Project $dir====="

   tail -n +2 scoutReports/$dir/scoutsuite-results/scoutsuite_results_$dir.js | jq '.' | jq --arg dir "$dir" '
if (
  (.services.bigquery.findings."bigquery-dataset-allAuthenticatedUsers".flagged_items > 0 or .services.bigquery.findings."bigquery-dataset-allUsers".flagged_items > 0)
)
then $dir
else empty
end'


done