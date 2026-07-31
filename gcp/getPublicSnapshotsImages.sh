#!/bin/bash
#
# check_public_snapshots.sh
#
# Loops through all accessible GCP projects and checks compute snapshots
# and images for public IAM bindings (allUsers / allAuthenticatedUsers).
#
# Usage: ./check_public_snapshots.sh
# Optional: pass a single project ID as $1 to check just one project
#   ./check_public_snapshots.sh my-project-id

set -uo pipefail

PUBLIC_PRINCIPALS="allUsers|allAuthenticatedUsers"
FOUND_ANY=0

if [ -n "${1:-}" ]; then
  PROJECTS="$1"
else
  PROJECTS=$(gcloud projects list --format="value(projectId)")
fi

for PROJECT in $PROJECTS; do
  echo "=== Checking project: $PROJECT ==="

  # --- Snapshots ---
  SNAPSHOTS=$(gcloud compute snapshots list --project="$PROJECT" --format="value(name)" 2>/dev/null)
  for SNAP in $SNAPSHOTS; do
    POLICY=$(gcloud compute snapshots get-iam-policy "$SNAP" --project="$PROJECT" --format=json 2>/dev/null)
    if echo "$POLICY" | grep -qE "$PUBLIC_PRINCIPALS"; then
      echo "  [!] PUBLIC SNAPSHOT: $SNAP (project: $PROJECT)"
      echo "$POLICY" | grep -E "$PUBLIC_PRINCIPALS" | sed 's/^/        /'
      FOUND_ANY=1
    fi
  done

  # --- Images ---
  IMAGES=$(gcloud compute images list --project="$PROJECT" --format="value(name)" 2>/dev/null)
  for IMG in $IMAGES; do
    POLICY=$(gcloud compute images get-iam-policy "$IMG" --project="$PROJECT" --format=json 2>/dev/null)
    if echo "$POLICY" | grep -qE "$PUBLIC_PRINCIPALS"; then
      echo "  [!] PUBLIC IMAGE: $IMG (project: $PROJECT)"
      echo "$POLICY" | grep -E "$PUBLIC_PRINCIPALS" | sed 's/^/        /'
      FOUND_ANY=1
    fi
  done

done

echo ""
if [ "$FOUND_ANY" -eq 0 ]; then
  echo "No publicly shared snapshots or images found."
else
  echo "Public snapshots/images were found above — review and remediate IAM bindings."
fi
