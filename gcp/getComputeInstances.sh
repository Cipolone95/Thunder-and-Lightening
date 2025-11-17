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
  echo "====Checking Publically Exposed Databases from GCP Project $dir====="

   tail -n +2 scoutReports/$dir/scoutsuite-results/scoutsuite_results_$dir.js | jq '.' | jq '
if (
  .services.computeengine.findings."computeengine-instance-public-ip-adresses".flagged_items > 0
)
then "Project Contains Publically accessible compute instances"
else "not vulnerable"
end'


done