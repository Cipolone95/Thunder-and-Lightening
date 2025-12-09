import json
import re
import sys
import argparse
from pathlib import Path


#Logic for parsing the scoutsuite file for s3 related checks.
#This is to help separate the code from all being lumped together. 

def getRootLoginInformation(finding, data):
    rootLoginInfo = []
    fieldList = [
        "access_key_1_active",
        "access_key_1_last_rotated",
        "access_key_1_last_used_date",
        "access_key_1_last_used_region",
        "access_key_1_last_used_service",
        "access_key_2_active",
        "access_key_2_last_rotated",
        "access_key_2_last_used_date",
        "access_key_2_last_used_region",
        "access_key_2_last_used_service"
    ]

    vulnerableResourceNames = []
    vulnerableResources = finding.get("items",[])
    #print(vulnerableResources)
    for resource in vulnerableResources: 
        #print(resourceBase)
        parts = resource.split(".")
        resourcePath = data.get("services", {})
        for p in parts:
            resourcePath = resourcePath.get(p, {})
        
        for field in fieldList:
            resourceName = resourcePath.get(field, {})
            vulnerableResourceNames.append(f"{field}: {resourceName}")
    return vulnerableResourceNames 


def getStandardARNs(finding, check, data):
    vulnerableResourceNames = []
    vulnerableResources = finding.get("items",[])
    #print(vulnerableResources)
    for resource in vulnerableResources:
        resourceBase = ""
        if check == "iam-group-with-no-users":
            resourceBase = resource
        elif check in ("iam-managed-policy-allows-NotActions",
                        "iam-managed-policy-allows-iam-PassRole",
                        "iam-managed-policy-allows-sts-AssumeRole"):
            resourceBase = resource.rsplit(".", 3)[0]
        elif check == "iam-user-no-Active-key-rotation":
            resourceBase = resource.rsplit(".", 2)[0]
        else:
            resourceBase = resource.rsplit(".", 1)[0]
            
        #print(resourceBase)
        parts = resourceBase.split(".")
        resourcePath = data.get("services", {})
        for p in parts:
            resourcePath = resourcePath.get(p, {})
        resourceName = resourcePath.get("arn", {})
        vulnerableResourceNames.append(resourceName)
    return list(set(vulnerableResourceNames)) 


def getResources(data, service, check):
    findings = data.get("services", {}).get(service, {}).get("findings", {})
    #projects = data.get("services", {}).get(service, {}).get("projects", {})
    finding = findings.get(check, {})
    vulnerableResourceNames = []
    #print(finding)
    #flagged = finding.get("flagged_items", [])


    
    if check in ("iam-group-with-no-users",
                    "iam-inline-group-policy-allows-NotActions",
                    "iam-managed-policy-allows-NotActions",
                    "iam-managed-policy-allows-iam-PassRole",
                    "iam-managed-policy-allows-sts-AssumeRole",
                    "iam-role-with-inline-policies",
                    "iam-root-account-no-mfa",
                    "iam-user-no-Active-key-rotation",
                    "iam-user-with-multiple-access-keys",
                    "iam-user-with-password-and-key",
                    "iam-user-without-mfa"):
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-root-account-with-active-keys":
        vulnerableResourceNames = getRootLoginInformation(finding, data)
    else:
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    
    
    return vulnerableResourceNames
    