#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""
AWS_ACCOUNTS=$(wc -l < "$ACCOUNT_FILE")

# Role to assume in each account
ROLE_NAME=""
SESSION_NAME="session1"

counter=1
# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "===== Processing account: $ACCOUNT_ID ($counter/$AWS_ACCOUNTS) ====="

    ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

    # Assume the role and get temporary credentials
    CREDS_JSON=$(aws sts assume-role \
        --role-arn "$ROLE_ARN" \
        --role-session-name "$SESSION_NAME" \
        --output json 2>/dev/null --profile test)

    if [ $? -ne 0 ]; then
        echo "❌ Failed to assume role for account $ACCOUNT_ID"
        echo 
        ((counter++))
        continue
    fi

    export AWS_ACCESS_KEY_ID=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
    export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretAccessKey')
    export AWS_SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')

    

   
    

    echo "✅ ECS Enumeration completed for account $ACCOUNT_ID"
    echo
    ((counter++))
done < "$ACCOUNT_FILE"


