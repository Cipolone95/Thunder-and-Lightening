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

echo "====Projects with Privileged Service Accounts====="

# Loop through and print each directory name
for dir in "${dir_list[@]}"; do
  #echo "====Checking Privileged Service Accounts from GCP Project $dir====="

#    tail -n +2 scoutReports/$dir/scoutsuite-results/scoutsuite_results_$dir.js | jq '.' | jq --arg dir "$dir" '
# if (
#   .services.iam.findings."iam-sa-has-admin-privileges".flagged_items > 0
# )
# then $dir
# else empty
# end'


echo "==== Project $dir====="

gcloud projects get-iam-policy $dir --filter "bindings.members:serviceAccount: AND (bindings.role:roles/owner OR bindings.role:roles/editor OR bindings.role:*.admin)" \
  --format="table(bindings.members, bindings.role)" --flatten="bindings[].members"

done