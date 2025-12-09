import json
import re
import sys
import argparse
from pathlib import Path

import variables
import s3
import iam
import kms
import ec2
import rds
import sns
import cloudtrail

def load_scoutsuite_js(path):
    """
    Load ScoutSuite JS file by stripping the var assignment and parsing the JSON.
    """
    with open(path, "r") as f:
        data = f.read()

    # Remove "var scoutSuiteResults = " if present
    data = re.sub(r"scoutsuite_results\s*=", "", data.strip())
    # Remove trailing semicolon
    data = data.rstrip(";")
    
    return json.loads(data)

def writeOutputFile(outputDir, subDir, file, check, resources):
    #This code snippet writes the vulnerable resources for the specific check to the service file (s3.txt, ec2.txt, etc.) in the given scoutsuite directory.
    #Essentially sorts by service/directory
    outputDirectory = Path(outputDir)
    outputDirectory.mkdir(parents=True, exist_ok=True)
    if subDir != "":
        outputDirectory = outputDirectory / subDir
    fileName = f"{file}_checks.txt"
    filepath = outputDirectory / fileName
    filepath.touch(exist_ok=True)

    with open(filepath, "a") as f:
        f.write(check + "\n")
        for resource in resources:
            f.write(resource + "\n")
        f.write("\n")
    
    #This code snippet sorts by check and creates a master list of all the resources for each check.
    #This list becomes the affected assets list. 
    outputDirectory = outputDirectory / "AffectedAssets"
    if not outputDirectory.exists():
        outputDirectory.mkdir(parents=True, exist_ok=True)
    fileName = f"{check}.txt"
    filepath = outputDirectory / fileName
    filepath.touch(exist_ok=True)

    with open(filepath, "a") as f:
        f.write(subDir + "\n")
        for resource in resources:
            f.write(resource + "\n")
        f.write("\n")


def get_vulnerable_resources(outputDir, directory, data, service):
    findings = data.get("services", {}).get(service, {}).get("findings", {})
    resourceNames = []

    for check in getattr(variables, f"{service}_checks"):
        finding = findings.get(check, {})
        flagged = finding.get("flagged_items", 0)
        if (flagged > 0) or (check == "ec2-IMDSv1"):

            # Used for debugging
            # testCheckList = [
            # ]
            if check == "ec2-IMDSv1":
                print(f"[-] Checking for IMDSv1 in use.")
            else:
                print(f"[-] {service} vulnerable to check {check}")
            serviceObject = globals().get(service)
            method = getattr(serviceObject, "getResources")
            vulnerableResourceNames = method(data, service, check)
            
            if vulnerableResourceNames:
                for arn in vulnerableResourceNames:
                    print(arn)
                print("\n")
                writeOutputFile(outputDir, directory, service, check, vulnerableResourceNames)
            else:
                print("[!] No vulnerable resources found!")


    #return list(resourceNames)

def main():
    
    parser = argparse.ArgumentParser(description="Parses ScoutSuite data. This script reviews the scoutsuite data and collects info on the provided cloud service(s).")
    parser.add_argument("--input-file", help="Scoutsuite results JS file.")
    parser.add_argument("--input-directory", help="a directory containing all of the scoutsuite projects.")
    parser.add_argument("--account-list", help="A txt file containing a list of all AWS accounts you want checked. Helpful for splitting out data.")
    parser.add_argument("--output-directory", help="Specify an output file to dump all of the data. Default is stdOut.")
    parser.add_argument("--type", help="Comma separated list of services. All services will be checked if no specified. Available services are acm, awslambda, cloudformation, cloudtrail, cloudwatch, config, directconnect, ec2, efs, elasticache, elb, elbv2, emr, iam, kms, rds, redshift, route53, s3, secretsmanager, ses, sns, sqs, vpc")
    args = parser.parse_args()

    services = []
    
    #Either we pass in the services we want or we check all of them.
    if args.type:
        services = args.type.split(",")
    else:
        services = variables.allServices
    
    if args.input_file:
        data = load_scoutsuite_js(args.input_file)
        for service in services:
            print(f"[+] Checking service {service} for misconfigurations.")
            get_vulnerable_resources(args.output_directory, "", data, service)
    
    # if args.account_list and args.input_directory:
    #     accountFile = args.account_list
    #     baseDirectory = Path(args.input_directory)
    #     with open(accountFile, "r") as f:
    #         for account in f:
    #             accountID = account.strip()
    #             ScoutsuiteResultsFile = Path(baseDirectory, accountID, "scoutsuite-results", (f"scoutsuite_results_{accountID}.js"))
    #             data = load_scoutsuite_js(ScoutsuiteResultsFile)
    #             for service in services:
    #                 print(f"[+] Checking service {service} for misconfigurations.")
    #                 get_vulnerable_resources(args.output_directory, directory, data, service)

    
    # if args.input_directory:
    #     baseDirectory = Path(args.input_directory)
    #     for directory in baseDirectory.iterdir():
    #         if directory.is_directory() and directory != "AffectedAssets":
    #             ScoutsuiteResultsFile = Path(baseDirectory, directory, "scoutsuite-results", (f"scoutsuite_results_{directory}.js"))
    #             data = load_scoutsuite_js(ScoutsuiteResultsFile)
    #             for service in services:
    #                 print(f"[+] Checking service {service} for misconfigurations.")
    #                 get_vulnerable_resources(args.output_directory, directory, data, service)
    

        if args.input_directory:
            baseDirectory = Path(args.input_directory)
            accountIDList = []
            if args.account_list:
                accountFile = args.account_list
                with accountFile.open("r") as f:
                    accountID = line.strip()
                    accountIDList.append(accountID)
            else:
                for directory in baseDirectory.iterdir():
                    if directory.is_directory() and directory != "AffectedAssets":
                        accountIDList.append(accountID)
            
            for directory in accountIDList:
                ScoutsuiteResultsFile = Path(baseDirectory, directory, "scoutsuite-results", (f"scoutsuite_results_{directory}.js"))
                data = load_scoutsuite_js(ScoutsuiteResultsFile)
                for service in services:
                    print(f"[+] Checking service {service} for misconfigurations.")
                    get_vulnerable_resources(args.output_directory, directory, data, service)
                
    




    








if __name__ == "__main__":
    main()


