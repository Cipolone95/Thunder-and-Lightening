#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""


# Loop through each account ID from the file
while read -r ACCOUNT_ID; do

    echo "===== Processing account: $ACCOUNT_ID ====="


    aws codebuild list-source-credentials --profile $ACCOUNT_ID

    echo "✅ EC2 Instance Data Enumeration completed for account $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"

