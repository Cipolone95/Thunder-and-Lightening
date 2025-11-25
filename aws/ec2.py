import json
import re
import sys
import argparse
from pathlib import Path


#Logic for parsing the scoutsuite file for s3 related checks.
#This is to help separate the code from all being lumped together. 




def getStandardARNs(finding, check, data):
    vulnerableResourceNames = []
    vulnerableResources = finding.get("items",[])
    #print(vulnerableResources)
    for resource in vulnerableResources:

        if check in ("ec2-security-group-opens-RDP-port-to-all",
                        "ec2-security-group-opens-SSH-port-to-all",
                        "ec2-security-group-opens-TCP-port-to-all",
                        "ec2-security-group-whitelists-aws"):
                        
            resourceBase = resource.rsplit(".", 9)[0]
        elif check in ("ec2-security-group-opens-all-ports",
                        "ec2-security-group-opens-plaintext-port-FTP",
                        "ec2-security-group-opens-port-range"):
            resourceBase = resource.rsplit(".", 6)[0]
        elif check == "ec2-security-group-opens-all-ports-to-self":
            resourceBase = resource.rsplit(".", 8)[0]
        elif check == "ec2-unused-security-group":
            resourceBase = resource
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


    if check in ("ec2-default-security-group-with-rules",
                    "ec2-ebs-snapshot-not-encrypted",
                    "ec2-ebs-volume-not-encrypted",
                    "ec2-security-group-opens-RDP-port-to-all",
                    "ec2-security-group-opens-SSH-port-to-all",
                    "ec2-security-group-opens-TCP-port-to-all",
                    "ec2-security-group-opens-all-ports",
                    "ec2-security-group-opens-all-ports-to-self",
                    "ec2-security-group-opens-plaintext-port-FTP",
                    "ec2-security-group-opens-port-range",
                    "ec2-security-group-whitelists-aws",
                    "ec2-unused-security-group"):
        vulnerableResourceNames = getStandardARNs(finding, check, data)
    else:
        print(f"[!] HELP! {check} is a new check and needs some logic!")
    
    return vulnerableResourceNames
    