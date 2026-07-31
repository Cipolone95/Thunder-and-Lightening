#!/usr/bin/env bash
#
# check_pubsub.sh
# Checks for existence of Pub/Sub topics and subscriptions across many GCP projects.
#
# Usage:
#   ./check_pubsub.sh projects.txt
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
  # Skip blank lines and comments
  [[ -z "$PROJECT" || "$PROJECT" =~ ^# ]] && continue

  echo "=============================================="
  echo "Project: $PROJECT"
  echo "=============================================="

  # --- Topics ---
  echo "--- Pub/Sub Topics ---"
  TOPICS=$(gcloud pubsub topics list --project="$PROJECT" --format="value(name)" 2>&1)
  TOPICS_STATUS=$?

  if [[ $TOPICS_STATUS -ne 0 ]]; then
    echo "ERROR retrieving topics (check permissions/project ID): $TOPICS"
  elif [[ -z "$TOPICS" ]]; then
    echo "No topics found."
  else
    echo "$TOPICS"
    echo "Topic count: $(echo "$TOPICS" | wc -l)"
  fi

  echo ""

  # --- Subscriptions ---
  echo "--- Pub/Sub Subscriptions ---"
  SUBS=$(gcloud pubsub subscriptions list --project="$PROJECT" --format="value(name)" 2>&1)
  SUBS_STATUS=$?

  if [[ $SUBS_STATUS -ne 0 ]]; then
    echo "ERROR retrieving subscriptions (check permissions/project ID): $SUBS"
  elif [[ -z "$SUBS" ]]; then
    echo "No subscriptions found."
  else
    echo "$SUBS"
    echo "Subscription count: $(echo "$SUBS" | wc -l)"
  fi

  echo ""
done < "$PROJECTS_FILE"

echo "Done."
