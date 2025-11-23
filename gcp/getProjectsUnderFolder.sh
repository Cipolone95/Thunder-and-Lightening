#!/usr/bin/env bash
set -euo pipefail

ROOT_FOLDER_ID="$1"  # numeric, e.g. 123456789012

# Get all descendant folders (including the root)
get_all_folders() {
  local parent_folder="$1"
  echo "$parent_folder"
  # List direct children
  gcloud resource-manager folders list \
    --folder="$parent_folder" \
    --format="value(name)" | while read -r child; do
      # child is like "folders/123456789012"
      local child_id="${child#folders/}"
      get_all_folders "$child_id"
  done
}

# Collect all folders under the root
folders=()
while read -r fid; do
  folders+=("$fid")
done < <(get_all_folders "$ROOT_FOLDER_ID" | sort -u)

# For each folder, list projects whose *immediate* parent is that folder
for fid in "${folders[@]}"; do
  gcloud projects list \
    --filter="parent.type:folder AND parent.id=$fid" \
    --format="value(projectId)"
done
