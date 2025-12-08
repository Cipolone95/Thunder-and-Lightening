#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""
AWS_ACCOUNTS=$(wc -l < "$ACCOUNT_FILE")


counter=1
# Loop through each account ID from the file
while read -r ACCOUNT_ID; do


    echo "===== Processing account: $ACCOUNT_ID ($counter/$AWS_ACCOUNTS) ====="



    echo "✅ ECS Enumeration completed for account $ACCOUNT_ID"
    echo
    ((counter++))
done < "$ACCOUNT_FILE"


