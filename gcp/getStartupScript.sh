#!/bin/bash

# Input file containing one project ID per line
PROJECT_FILE="projectIDPete.txt"

# Output directory
OUTPUT_DIR="startup_scripts_output"
mkdir -p "$OUTPUT_DIR"

while read -r PROJECT; do
    [[ -z "$PROJECT" ]] && continue

    echo "[+] Processing Project: $PROJECT"
    mkdir -p "$OUTPUT_DIR/$PROJECT"

    # Get all zones containing instances
    ZONES=$(gcloud compute instances list \
        --project="$PROJECT" \
        --format="value(zone)" --quiet | sort -u)

    # Get project-level startup script (if any)
    PROJECT_SCRIPT=$(gcloud compute project-info describe \
        --project="$PROJECT" \
        --format="value(commonInstanceMetadata.items.startup-script)" --quiet)

    if [[ -n "$PROJECT_SCRIPT" ]]; then
        echo "[+] Found project-level startup script for $PROJECT"
        echo "$PROJECT_SCRIPT" > "$OUTPUT_DIR/$PROJECT/project_startup_script.txt"
    fi

    # Loop through each zone
    for ZONE in $ZONES; do
        echo "  [+] Zone: $ZONE"

        INSTANCES=$(gcloud compute instances list \
            --project="$PROJECT" \
            --zones="$ZONE" \
            --format="value(name)" --quiet)

        # Loop through each instance
        for INSTANCE in $INSTANCES; do
            echo "    [+] Instance: $INSTANCE"

            SCRIPT=$(gcloud compute instances describe "$INSTANCE" \
                --project="$PROJECT" \
                --zone="$ZONE" \
                --format="value(metadata.items.startup-script)" --quiet)

            # Save script if present
            if [[ -n "$SCRIPT" ]]; then
                OUTFILE="$OUTPUT_DIR/$PROJECT/${INSTANCE}_startup_script.txt"
                echo "$SCRIPT" > "$OUTFILE"
                echo "      [-] Saved: $OUTFILE"
            else
                echo "      [-] No startup-script metadata"
            fi
        done
    done

done < "$PROJECT_FILE"

echo "[+] Finished. Output saved in $OUTPUT_DIR/"
