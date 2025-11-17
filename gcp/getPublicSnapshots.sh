#!/bin/bash

# Path to file with GCP account IDs (one per line)
ACCOUNT_FILE="projectIDs.txt"


# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "===== Processing Project: $ACCOUNT_ID ====="

    for s in $(gcloud compute snapshots list --project $ACCOUNT_ID --format="value(name)" --quiet); do
    gcloud compute snapshots get-iam-policy $s \
        --project $ACCOUNT_ID --format=json | jq 'select(.bindings[].members[] == "allUsers" or .bindings[].members[] == "allAuthenticatedUsers")'
    done



    #echo "✅ Scout Suite completed for Project $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"
