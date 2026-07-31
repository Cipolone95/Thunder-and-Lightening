#!/bin/bash
#
# Usage:
#   ./script.sh <projectIDs_file> <domain_to_exclude>
#
# Example:
#   ./script.sh projectIDs.txt example.com
 
# --- Argument handling ---
if [[ $# -ne 2 ]]; then
    echo "Usage: $0 <projectIDs_file> <domain_to_exclude>"
    exit 1
fi
 
ACCOUNT_FILE="$1"
DOMAIN="$2"
 
if [[ ! -f "$ACCOUNT_FILE" ]]; then
    echo "ERROR: File '$ACCOUNT_FILE' not found."
    exit 1
fi
 
# Loop through each account ID from the file
while read -r ACCOUNT_ID; do
    # Skip empty lines or lines that start with #
    [[ -z "$ACCOUNT_ID" || "$ACCOUNT_ID" =~ ^# ]] && continue
    echo "===== Project: $ACCOUNT_ID ====="
    # Run Scout Suite
    gcloud projects get-iam-policy "$ACCOUNT_ID" --format="table(bindings.role, bindings.members)" \
     --flatten="bindings[].members" \
     --filter="NOT bindings.members:*gserviceaccount.com AND NOT bindings.members:*${DOMAIN}"
    #echo "✅ Scout Suite completed for Project $ACCOUNT_ID"
    echo
done < "$ACCOUNT_FILE"
 
