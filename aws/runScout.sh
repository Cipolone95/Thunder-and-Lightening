#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""

# Role to assume in each account
ROLE_NAME=""
SESSION_NAME="session1"

# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "===== Processing account: $ACCOUNT_ID ====="

    ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

    # Assume the role and get temporary credentials
    CREDS_JSON=$(aws sts assume-role \
        --role-arn "$ROLE_ARN" \
        --role-session-name "$SESSION_NAME" \
        --output json 2>/dev/null --profile test)

    if [ $? -ne 0 ]; then
        echo "❌ Failed to assume role for account $ACCOUNT_ID"
        continue
    fi

    echo $CREDS_JSON

    AWS_ACCESS_KEY_ID=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
    AWS_SECRET_ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretAccessKey')
    AWS_SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')

    # Create output directory
    OUTPUT_DIR="scoutReports/${ACCOUNT_ID}"
    #mkdir -p "$OUTPUT_DIR"

    # Run Scout Suite
    scout aws --report-dir "$OUTPUT_DIR" --access-keys --access-key-id $AWS_ACCESS_KEY_ID --secret-access-key $AWS_SECRET_ACCESS_KEY --session-token $AWS_SESSION_TOKEN --max-workers 6 --no-browser

    echo "✅ Scout Suite completed for account $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"

# Cleanup
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
