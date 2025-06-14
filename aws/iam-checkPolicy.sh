#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 -p <PROFILE>"
    exit 1
}

# Parse parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -p)
            PROFILE="$2"
            shift 2
            ;;
        *)
            echo "Invalid parameter: $1"
            usage
            ;;
    esac
done

# Ensure parameters are provided
if [[ -z "$PROFILE" ]]; then
    echo "Error: Missing required parameters."
    usage
fi


username="$(aws sts get-caller-identity --profile "$PROFILE" | jq -r '.Arn | split("/") | last')"
echo "[+] Username is $username"

policyARN="$(aws --profile="$PROFILE" iam list-attached-user-policies --user-name "$username" | jq -r '.AttachedPolicies[0].PolicyArn')"
echo "[+] Policy ARN is $policyARN"

versionID="$(aws --profile "$PROFILE" iam get-policy --policy-arn "$policyARN" | jq -r '.Policy.DefaultVersionId')"
echo "[+] Default Version ID is $versionID"
echo "[+] Attempting to retrieve the policy"

if ! aws --profile "$PROFILE" iam get-policy-version --policy-arn "$policyARN" --version-id "$versionID"; then
    echo "[-] Error: Failed to retrieve user policy"
    exit 1
fi


