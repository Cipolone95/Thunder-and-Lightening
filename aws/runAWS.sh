#!/usr/bin/env bash

# Default values
PROFILE=""
ACCOUNT_FILE=""
AWS_CONFIG_FILE="$HOME/.aws/config"
SSO=false
SSO_SESSION=""
SSO_ROLE_NAME="AWSReadOnlyAccess"
SSO_REGION=""
SSO_OUTPUT="json"
ASSUME_ROLE_NAME=""


# Role name, region, and output format

region="us-east-1" #replace with region
output="json"

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --profile)
            PROFILE="$2"
            shift 2
            ;;
        --assume-role)
            ASSUME_ROLE_NAME="$2"
            shift 2
            ;;
        --sso-name)
            SSO_SESSION="$2"
            shift 2
            ;;
        --accounts)
            ACCOUNT_FILE="$2"
            shift 2
            ;;
        --sso)
            SSO=true
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Output results
# if [[ -n "$PROFILE" ]]; then
#     echo "Profile: $PROFILE"
# fi

# if [[ -n "$ASSUME_ROLE_NAME" ]]; then
#     echo "Key: $KEY"
# fi

if [[ "$SSO" == true ]]; then
    if [[ -z "$SSO_SESSION" ]]; then
        SSO_SESSION="session1"
    fi

    if [[ -z "$SSO_REGION" ]]; then
        SSO_REGION="us-east-1"
    fi

    #Backup the config file in case something gets scuffed
    cp "$AWS_CONFIG_FILE" "$AWS_CONFIG_FILE.bak.$(date +%s)"

    # Read each account ID from the file and create a profile
    while IFS= read -r ACCOUNT_ID; do
    # Skip empty lines
    [ -z "$account_id" ] && continue

    cat <<EOF >> "$AWS_CONFIG_FILE"
[profile $ACCOUNT_ID]
sso_session = $SSO_SESSION
sso_account_id = $ACCOUNT_ID
sso_role_name = $SSO_ROLE_NAME
region = $SSO_REGION
output = $SSO_OUTPUT
EOF

    done < "$ACCOUNT_FILE"
    echo "[+] AWS profiles have been added to $AWS_CONFIG_FILE."
fi

mkdir -p "scoutReports"

while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue

    echo "[+] Processing account: $ACCOUNT_ID"
    
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




