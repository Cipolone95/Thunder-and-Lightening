import json
import re
import sys
import argparse
from pathlib import Path


#Logic for parsing the scoutsuite file for s3 related checks.
#This is to help separate the code from all being lumped together. 


# def getStandardARNs(finding, data):
#     vulnerableResourceNames = []
#     vulnerableResources = finding.get("items",[])
#     for resource in vulnerableResources:
#         resourceBase = resource.rsplit(".", 1)[0]
#         parts = resourceBase.split(".")
#         resourcePath = data.get("services", {})
#         for p in parts:
#             resourcePath = resourcePath.get(p, {})
#         resourceName = resourcePath.get("arn", {})
#         vulnerableResourceNames.append(resourceName)
#     return vulnerableResourceNames 

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

    if check == "s3-bucket-AllUsers-read":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-AllUsers-read_acp":
        print(f"[!] HELP! {check} is a new check and needs some logic!")      
    elif check == "s3-bucket-AllUsers-write":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-AllUsers-write_acp":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-AuthenticatedUsers-read":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-AuthenticatedUsers-read_acp":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-AuthenticatedUsers-write":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-AuthenticatedUsers-write_acp":
        print(f"[!] HELP! {check} is a new check and needs some logic!")     
    elif check == "s3-bucket-allowing-cleartext":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "s3-bucket-no-default-encryption":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-no-logging":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "s3-bucket-no-mfa-delete":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "s3-bucket-no-versioning":
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    elif check == "s3-bucket-world-Delete-policy":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-world-Get-policy":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-world-List-policy":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-world-Manage-policy":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-world-Put-policy":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    elif check == "s3-bucket-world-policy-star":
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    else:
        print(test)
        #Do nothing at this point. 
    
    return vulnerableResourceNames
    