#!/usr/bin/env bash
#
# open_reports.sh
# Opens the ScoutSuite HTML report for each project listed in a file.
#
# Usage:
#   ./open_reports.sh projectIDs.txt

PROJECTS_FILE="${1:-projectIDs.txt}"

if [[ ! -f "$PROJECTS_FILE" ]]; then
  echo "ERROR: Projects file '$PROJECTS_FILE' not found." >&2
  exit 1
fi

while read -r PROJECT; do
  [[ -z "$PROJECT" || "$PROJECT" =~ ^# ]] && continue
  FILE="./scoutReports/${PROJECT}/${PROJECT}.html"
  if [[ -f "$FILE" ]]; then
    #open "$FILE"   # macOS
     xdg-open "$FILE"   # Linux (uncomment if on Linux)
  else
    echo "File not found: $FILE"
  fi
done < "$PROJECTS_FILE"
