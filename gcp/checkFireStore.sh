#!/usr/bin/env bash
#
# check_firestore_exists.sh
# Checks for existence of Firestore/Datastore databases across many GCP projects.
#
# Usage:
#   ./check_firestore_exists.sh projects.txt
#
# projects.txt should contain one GCP project ID per line (blank lines and lines
# starting with # are ignored).

set -uo pipefail

PROJECTS_FILE="${1:-projects.txt}"

if [[ ! -f "$PROJECTS_FILE" ]]; then
  echo "ERROR: Projects file '$PROJECTS_FILE' not found." >&2
  exit 1
fi

if ! command -v gcloud &>/dev/null; then
  echo "ERROR: gcloud CLI not found in PATH." >&2
  exit 1
fi

while IFS= read -r PROJECT || [[ -n "$PROJECT" ]]; do
  [[ -z "$PROJECT" || "$PROJECT" =~ ^# ]] && continue

  echo "=============================================="
  echo "Project: $PROJECT"
  echo "=============================================="

  DBS=$(gcloud firestore databases list --project="$PROJECT" \
        --format="table(name,type,locationId)" 2>&1)
  DBS_STATUS=$?

  if [[ $DBS_STATUS -ne 0 ]]; then
    if echo "$DBS" | grep -q "reason: SERVICE_DISABLED"; then
      echo "SERVICE DISABLED (Firestore/Datastore API not enabled for this project)"
    else
      echo "ERROR retrieving databases (check permissions/project ID): $DBS"
    fi
  elif [[ -z "$DBS" ]]; then
    echo "No Firestore/Datastore databases found."
  else
    echo "$DBS"
  fi

  echo ""
done < "$PROJECTS_FILE"

echo "Done."
