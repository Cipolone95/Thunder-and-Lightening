import json
import re
import sys
import argparse
from pathlib import Path


#Logic for parsing the scoutsuite file for s3 related checks.
#This is to help separate the code from all being lumped together. 

def getResources(data, service, check):
    findings = data.get("services", {}).get(service, {}).get("findings", {})
    #projects = data.get("services", {}).get(service, {}).get("projects", {})
    finding = findings.get(check, {})
    vulnerableResourceNames = []
    #print(finding)
    #flagged = finding.get("flagged_items", [])

    if check == "s3-bucket-AllUsers-read":
        print(test)
    elif check == "s3-bucket-AllUsers-read_acp":
        print(test)        
    elif check == "s3-bucket-AllUsers-write":
        print(test)
    elif check == "s3-bucket-AllUsers-write_acp":
        print(test)
    elif check == "s3-bucket-AuthenticatedUsers-read":
        print(test)
    elif check == "s3-bucket-AuthenticatedUsers-read_acp":
        print(test)
    elif check == "s3-bucket-AuthenticatedUsers-write":
        print(test)
    elif check == "s3-bucket-AuthenticatedUsers-write_acp":
        # vulnerableResources = finding.get("items",[])
        # for resource in vulnerableResources:
        #         resourceBase = resource.rsplit(".", 1)[0]
        #         parts = resourceBase.split(".")
        #         resourcePath = data.get("services", {})
        #         for p in parts:
        #             resourcePath = resourcePath.get(p, {})
        #         resourceName = resourcePath.get("members", {}).get("service_accounts", {})
                
        #         for name in resourceName:
        #             vulnerableResourceNames.append(name)  
        # return vulnerableResourceNames 
        print(test)      
    elif check == "s3-bucket-allowing-cleartext":
        vulnerableResources = finding.get("items",[])
        for resource in vulnerableResources:
                resourceBase = resource.rsplit(".", 1)[0]
                parts = resourceBase.split(".")
                resourcePath = data.get("services", {})
                for p in parts:
                    resourcePath = resourcePath.get(p, {})
                resourceName = resourcePath.get("arn", {})
                vulnerableResourceNames.append(resourceName) 
    elif check == "s3-bucket-no-default-encryption":
        print(test)
    elif check == "s3-bucket-no-logging":
        print(test)
    elif check == "s3-bucket-no-mfa-delete":
        print(test)
    elif check == "s3-bucket-no-versioning":
        print(test)
    elif check == "s3-bucket-world-Delete-policy":
        print(test)
    elif check == "s3-bucket-world-Get-policy":
        print(test)
    elif check == "s3-bucket-world-List-policy":
        print(test)
    elif check == "s3-bucket-world-Manage-policy":
        print(test)
    elif check == "s3-bucket-world-Put-policy":
        print(test)
    elif check == "s3-bucket-world-policy-star":
        print(test)
    else:
        print(test)
        #Do nothing at this point. 
    
    return vulnerableResourceNames
    