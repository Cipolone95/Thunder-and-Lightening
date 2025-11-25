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


    if check == "iam-assume-role-lacks-external-id-and-mfa":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-assume-role-policy-allows-all":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-ec2-role-without-instances":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-group-with-inline-policies":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-group-with-no-users":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-inline-group-policy-allows-NotActions":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-inline-group-policy-allows-iam-PassRole":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-group-policy-allows-sts-AssumeRole":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-role-policy-allows-NotActions":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-role-policy-allows-iam-PassRole":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-role-policy-allows-sts-AssumeRole":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-user-policy-allows-NotActions":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-user-policy-allows-iam-PassRole":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-inline-user-policy-allows-sts-AssumeRole":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-managed-policy-allows-NotActions":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-managed-policy-allows-iam-PassRole":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-managed-policy-allows-sts-AssumeRole":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-managed-policy-no-attachments":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-password-policy-minimum-length":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-password-policy-no-expiration":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-password-policy-reuse-enabled":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-role-with-inline-policies":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-root-account-no-mfa":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-root-account-used-recently":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-root-account-with-active-certs":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-root-account-with-active-keys":
        vulnerableResourceNames = getRootLoginInformation(finding, data)
    elif check == "iam-user-no-Active-key-rotation":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-user-no-Inactive-key-rotation":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-user-with-inline-policies":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "iam-user-with-multiple-access-keys":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-user-with-password-and-key":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "iam-user-without-mfa":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    else:
        print(f"[+] {check} is handled elsewhere.") 
    
    return vulnerableResourceNames
    