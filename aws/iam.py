import json
import re
import sys
import argparse
from pathlib import Path


#Logic for parsing the scoutsuite file for iam related checks.
#This is to help separate the code from all being lumped together. 

def getResources(data, service, check):
    findings = data.get("services", {}).get(service, {}).get("findings", {})
    projects = data.get("services", {}).get(service, {}).get("projects", {})
    finding = findings.get(check, {})
    vulnerableResourceNames = []
    #print(finding)
    #flagged = finding.get("flagged_items", [])

    if check == "iam-gmail-accounts-used":
        print(test)
    elif check == "iam-lack-of-service-account-key-rotation":
        
        vulnerableResources = finding.get("items",[])
        for resource in vulnerableResources:
                resourceBase = resource.rsplit(".", 1)[0]
                parts = resourceBase.split(".")
                resourcePath = data.get("services", {})
                for p in parts:
                    resourcePath = resourcePath.get(p, {})
                resourceName = resourcePath.get("id", {})
                vulnerableResourceNames.append(resourceName)         
    elif check == "iam-primitive-role-in-use":
        print(test)
    elif check == "iam-role-account-separation-duties-is-false":
        print(test)
    elif check == "iam-role-assigned-to-domain":
        print(test)
    elif check == "iam-role-assigned-to-user":
        print(test)
    elif check == "iam-role-kms-separation-duties-is-false":
        print(test)
    elif check == "iam-sa-has-admin-privileges":
        vulnerableResources = finding.get("items",[])
        for resource in vulnerableResources:
                resourceBase = resource.rsplit(".", 1)[0]
                parts = resourceBase.split(".")
                resourcePath = data.get("services", {})
                for p in parts:
                    resourcePath = resourcePath.get(p, {})
                resourceName = resourcePath.get("members", {}).get("service_accounts", {})
                
                for name in resourceName:
                    vulnerableResourceNames.append(name)  
        return vulnerableResourceNames       
    elif check == "iam-service-account-user-allAuthenticatedUsers":
        print(test)
    elif check == "iam-service-account-user-allUsers":
        print(test)
    elif check == "iam-service-account-with-user-managed-keys":
        print(test)
    elif check == "iam-user-has-sa-user-role":
        print(test)
    else:
        print(test)
        #Do nothing at this point. 
    
    return vulnerableResourceNames
    