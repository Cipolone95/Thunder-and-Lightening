#!/bin/bash

# Path to file with AWS account IDs (one per line)
ACCOUNT_FILE=""


# Loop through each account ID from the file
while read -r ACCOUNT_ID; do

    echo "===== Processing account: $ACCOUNT_ID ====="

    

    for region in us-east-1; do
        for instanceid in $(aws ec2 describe-instances --region $region --profile $ACCOUNT_ID | grep -Eo '"i-[a-zA-Z0-9]+' | tr -d '"'); do
            echo "Instance ID: $instanceid"
            aws ec2 describe-instance-attribute --profile $ACCOUNT_ID --region $region --instance-id "$instanceid" --attribute userData | jq ".UserData.Value" | tr -d '"' | base64 -d
            echo ""
            echo "-------------------"
        done
    done




    echo "✅ EC2 Instance Data Enumeration completed for account $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"

