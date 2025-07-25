#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""

# Role to assume in each account
ROLE_NAME="AWSReadOnlyAccess"
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

    export AWS_ACCESS_KEY_ID=$(echo "$CREDS_JSON" | jq -r '.Credentials.AccessKeyId')
    export AWS_SECRET_ACCESS_KEY=$(echo "$CREDS_JSON" | jq -r '.Credentials.SecretAccessKey')
    export AWS_SESSION_TOKEN=$(echo "$CREDS_JSON" | jq -r '.Credentials.SessionToken')

    # Create output directory
    OUTPUT_DIR="EC2Data/${ACCOUNT_ID}"
    #mkdir -p "$OUTPUT_DIR"

    for region in us-east-1 us-east-2 us-west-1 us-west-2; do
        for instanceid in $(aws ec2 describe-instances --region $region | grep -Eo '"i-[a-zA-Z0-9]+' | tr -d '"'); do
            echo "Instance ID: $instanceid"
            aws ec2 describe-instance-attribute --region $region --instance-id "$instanceid" --attribute userData | jq ".UserData.Value" | tr -d '"' | base64 -d
            echo ""
            echo "-------------------"
        done
    done




    echo "✅ EC2 Instance Data Enumeration completed for account $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"

# Cleanup
unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN
