#!/usr/bin/env bash
#
# check_databases.sh
# Checks for existence of GCP database services across many projects:
#   Cloud SQL, Cloud Spanner, AlloyDB, Firestore/Datastore, Bigtable,
#   Memorystore (Redis + Memcached), BigQuery, Bare Metal Solution (Oracle)
#
# Usage:
#   ./check_databases.sh projectIDs.txt

set -uo pipefail

PROJECTS_FILE="${1:-projectIDPete.txt}"

if [[ ! -f "$PROJECTS_FILE" ]]; then
  echo "ERROR: Projects file '$PROJECTS_FILE' not found." >&2
  exit 1
fi

if ! command -v gcloud &>/dev/null; then
  echo "ERROR: gcloud CLI not found in PATH." >&2
  exit 1
fi

# Helper: run a command, report SERVICE_DISABLED / errors / empty / results
check() {
  local label="$1"
  local output
  local status

  output=$(eval "$2" 2>&1)
  status=$?

  echo "--- $label ---"
  if [[ $status -ne 0 ]]; then
    if echo "$output" | grep -q "reason: SERVICE_DISABLED"; then
      echo "SERVICE DISABLED"
    else
      echo "ERROR: $output"
    fi
  elif [[ -z "$output" ]]; then
    echo "None found."
  else
    echo "$output"
  fi
  echo ""
}

while IFS= read -r PROJECT || [[ -n "$PROJECT" ]]; do
  [[ -z "$PROJECT" || "$PROJECT" =~ ^# ]] && continue

  echo "=============================================="
  echo "Project: $PROJECT"
  echo "=============================================="

  check "Cloud SQL" \
    "gcloud sql instances list --project=$PROJECT --format='value(name)'"

  check "Cloud Spanner" \
    "gcloud spanner instances list --project=$PROJECT --format='value(name)'"

  check "AlloyDB" \
    "gcloud alloydb clusters list --project=$PROJECT --region=- --format='value(name)'"

  check "Firestore / Datastore" \
    "gcloud firestore databases list --project=$PROJECT --format='value(name)'"

  check "Bigtable" \
    "gcloud bigtable instances list --project=$PROJECT --format='value(name)'"

  check "Memorystore (Redis)" \
    "gcloud redis instances list --project=$PROJECT --region=us-central1 --format='value(name)'"

  check "Memorystore (Memcached)" \
    "gcloud memcache instances list --project=$PROJECT --region=us-central1 --format='value(name)'"

  


done < "$PROJECTS_FILE"

echo "Done."
