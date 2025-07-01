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


echo "[+] Atempting to run: Get Caller Identity"
if username="$(aws sts get-caller-identity --profile "$PROFILE" | jq -r '.Arn | split("/") | last')"; then
    echo "[+] Username is $username"
else
    echo "[-] Error: Could not get username"
fi

echo "[+] Atempting to run: List Inline User Policies"
if inlinePolicyARN="$(aws iam list-user-policies --profile "$PROFILE" --user-name "$username" | jq -r '.PolicyNames[]')"; then
    echo "[+] Inline policy is $inlinePolicyARN"
else
    echo "[-] Error: Could not get inline policies"
fi

echo "[+] Atempting to run: List Attached User Policies"
if policyARN="$(aws --profile="$PROFILE" iam list-attached-user-policies --user-name "$username" | jq -r '.AttachedPolicies[0].PolicyArn')"; then
    echo "[+] Policy ARN is $policyARN"
else
    echo "[-] Error: Could not get Attached User Policies"
fi


echo "[+] Attempting to retrieve the policy"
versionID="$(aws --profile "$PROFILE" iam get-policy --policy-arn "$policyARN" | jq -r '.Policy.DefaultVersionId')"
echo "[+] Default Version ID is $versionID"



if policy="$(aws --profile "$PROFILE" iam get-policy-version --policy-arn "$policyARN" --version-id "$versionID")"; then
    echo "[+] Policy is $policy"
else
    echo "[-] Error: Could not get policy information"
fi