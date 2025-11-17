#!/bin/bash

############################
# Run this tool to find Cloud Functions that permit unauthenticated invocations
# anywhere in your GCP organization.
# Enjoy!
############################

for proj in $(gcloud projects list --format="get(projectId)"); do
    echo "[*] scraping project $proj"

    enabled=$(gcloud services list --project "$proj" | grep "Cloud Functions API")

    if [ -z "$enabled" ]; then
    continue
    fi


    for func_region in $(gcloud functions list --quiet --project "$proj" --format="value[separator=','](NAME,REGION)"); do
        # drop substring from first occurence of "," to end of string.
        func="${func_region%%,*}"
        # drop substring from start of string up to last occurence of ","
        region="${func_region##*,}"
        ACL="$(gcloud functions get-iam-policy "$func" --project "$proj" --region "$region")"

        all_users="$(echo "$ACL" | grep allUsers)"
        all_auth="$(echo "$ACL" | grep allAuthenticatedUsers)"

        if [ -z "$all_users" ]
        then
              :
        else
              echo "[!] Open to all users: $proj: $func"
        fi

        if [ -z "$all_auth" ]
        then
              :
        else
              echo "[!] Open to all authenticated users: $proj: $func"
        fi
    done
done
