#!/bin/bash
while read -r project; do
  echo "=== $project ==="
  default_header_written=false
  custom_header_written=false

  gcloud projects get-iam-policy "$project" \
    --flatten="bindings[].members" \
    --filter="bindings.role:(roles/owner OR roles/editor) AND bindings.members:serviceAccount" \
    --format="value(bindings.members,bindings.role)" 2>/dev/null | \
  while IFS=$'\t' read -r member role; do
    email="${member#serviceAccount:}"
    if [[ "$email" == *"@cloudservices.gserviceaccount.com" ]] || \
       [[ "$email" == *"-compute@developer.gserviceaccount.com" ]] || \
       [[ "$email" == *"@appspot.gserviceaccount.com" ]] || \
       [[ "$email" == *"@gcp-sa-"* ]]; then
      if [[ "$default_header_written" == false ]]; then
        echo "$project" >> default_sas2.txt
        default_header_written=true
      fi
      echo "$email" >> default_sas2.txt
    else
      if [[ "$custom_header_written" == false ]]; then
        echo "$project" >> custom_sas2.txt
        custom_header_written=true
      fi
      echo "$email" >> custom_sas2.txt
    fi
  done
done < projectIDs.txt
