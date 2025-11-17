#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE="projectIDs.txt"


# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "===== Project: $ACCOUNT_ID ====="


    # Run Scout Suite
    gcloud projects get-iam-policy $ACCOUNT_ID --format="table(bindings.role, bindings.members)" \
     --flatten="bindings[].members" \
     --filter="NOT bindings.members:*gserviceaccount.com"

    #echo "✅ Scout Suite completed for Project $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"

