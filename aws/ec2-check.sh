#!/bin/bash

# Usage function
usage() {
    echo "Usage: $0 -p <PROFILE> --file <FILE>"
    exit 1
}

# Parse parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -p)
            PROFILE="$2"
            shift 2
            ;;
        --file)
            FILE="$2"
            shift 2
            ;;
        *)
            echo "Invalid parameter: $1"
            usage
            ;;
    esac
done

# Ensure parameters are provided
if [[ -z "$PROFILE" || -z "$FILE" ]]; then
    echo "Error: Missing required parameters."
    usage
fi

# Ensure file exists
if [[ ! -f "$FILE" ]]; then
    echo "Error: File '$FILE' not found."
    exit 1
fi

# Loop through each region and run AWS command
while IFS= read -r REGION; do
    echo "Checking EC2 instances in region: $REGION"
    aws --profile "$PROFILE" ec2 describe-instances --region "$REGION"
done < "$FILE"
