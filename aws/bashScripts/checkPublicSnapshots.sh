#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""


# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "===== Checking for public snapshots in AWS account: $ACCOUNT_ID ====="

    userID=$(echo $ACCOUNT_ID | cut -d '-' -f2) 

    aws ec2 describe-snapshots --restorable-by-user-ids all --owner-ids $userID --profile $ACCOUNT_ID
done < "$ACCOUNT_FILE"

