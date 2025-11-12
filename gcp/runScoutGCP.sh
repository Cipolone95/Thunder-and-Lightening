#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE="projectIDs.txt"


# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "===== Processing Project: $ACCOUNT_ID ====="

    # Create output directory
    OUTPUT_DIR="scoutReports/${ACCOUNT_ID}"
    #mkdir -p "$OUTPUT_DIR"

    # Run Scout Suite
    scout gcp --report-dir "$OUTPUT_DIR" --report-name $ACCOUNT_ID --user-account --project-id $ACCOUNT_ID


    echo "✅ Scout Suite completed for Project $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"

