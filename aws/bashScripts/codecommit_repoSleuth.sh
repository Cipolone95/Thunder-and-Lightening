#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 -p <PROFILE> -r <REPOSITORY>"
    exit 1
}

# Initialize variables
PROFILE=""
REPOSITORY=""

# Parse parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -p)
            PROFILE="$2"
            shift 2
            ;;
        -r)
            REPOSITORY="$2"
            shift 2
            ;;
        *)
            echo "Invalid parameter: $1"
            usage
            ;;
    esac
done

# Check required parameters
if [[ -z "$PROFILE" || -z "$REPOSITORY" ]]; then
    usage
fi

# Ensure parameters are provided
if [[ -z "$PROFILE" ]]; then
    echo "Error: Missing required parameters."
    usage
fi

commit_id="$(aws --profile "$PROFILE" codecommit get-branch --repository-name "$REPOSITORY" --branch-name dev --query 'branch.commitId' --output text)"
echo "[+] Commit ID is $commit_id"


current=$commit_id

while [ "$current" != "None" ] && [ "$current" != "null" ]; do
    
    parentId="$(aws --profile "$PROFILE" codecommit get-commit --repository-name "$REPOSITORY" --commit-id "$current" --query 'commit.parents[0]' --output text)"
    echo "[+] Parent Commit ID is $parentId"
    
    
    echo "Scanning commit $current..."

    aws --profile "$PROFILE" codecommit get-commit --repository-name "$REPOSITORY" --commit-id "$current"

    files="$(aws --profile "$PROFILE" codecommit get-differences --repository-name "$REPOSITORY" --after-commit-specifier "$current" --before-commit-specifier "$parentId")"

    # Loop through files and fetch their content at this commit
    for path in $(echo "$files" | jq -r '.differences[].afterBlob.path'); do
        echo "[+] Printing File Contents of file $path"
        aws --profile "$PROFILE" codecommit get-file --repository-name "$REPOSITORY" --commit-specifier "$current" --file-path "$path" --output text | cut -d $'\t' -f 3 | base64 -d 

    done

    

    current=$parentId
done

