import json
import re
import sys
import argparse
from pathlib import Path

import variables
import s3
import iam
import kms

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

def writeOutputFile(path, file, check, resources):
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    fileName = f"{file}_checks.txt"
    filepath = directory / fileName
    filepath.touch(exist_ok=True)

    with open(filepath, "a") as f:
        f.write(check + "\n")
        for resource in resources:
            f.write(resource + "\n")
        f.write("\n")

def get_vulnerable_resources(outputDir, data, service):
    findings = data.get("services", {}).get(service, {}).get("findings", {})
    #projects = data.get("services", {}).get(service, {}).get("projects", {})
    resourceNames = []



    for check in getattr(variables, f"{service}_checks"):
        finding = findings.get(check, {})
        flagged = finding.get("flagged_items", 0)
        if flagged > 0:

            testCheckList = [
                # "iam-user-without-mfa",
                # "iam-root-account-no-mfa",
                # "iam-group-with-no-users",
                # "iam-managed-policy-allows-NotActions",
                # "iam-managed-policy-allows-iam-PassRole",
                # "iam-managed-policy-allows-sts-AssumeRole",
                # "iam-role-with-inline-policies",
                # "iam-root-account-with-active-keys",
                # "iam-user-no-Active-key-rotation",
                # "iam-user-with-multiple-access-keys",
                # "iam-user-with-password-and-key",
                # "iam-user-without-mfa",
                # "s3-bucket-allowing-cleartext",
                # "s3-bucket-no-logging",
                # "s3-bucket-no-mfa-delete",
                # "s3-bucket-no-versioning"
            ]

            print(f"[-] {service} vulnerable to check {check}")
            serviceObject = globals().get(service)
            method = getattr(serviceObject, "getResources")
            vulnerableResourceNames = method(data, service, check)
            for arn in vulnerableResourceNames:
                print(arn)
            print("\n")
            writeOutputFile(outputDir, service, check, vulnerableResourceNames)


    #return list(resourceNames)

def main():
    
    parser = argparse.ArgumentParser(description="Parses ScoutSuite data. This script reviews the scoutsuite data and collects info on the provided cloud service(s).")
    parser.add_argument("--input-file", help="Scoutsuite results JS file.")
    parser.add_argument("--input-directory", help="a directory containing all of the scoutsuite projects.")
    parser.add_argument("--project-list", help="A txt file containing a list of all projects you want checked. Helpful for splitting out data.")
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
            get_vulnerable_resources(args.output_directory, data, service)
    
    if args.project_list and args.input_directory:
        projectFile = args.project_list
        baseDirectory = Path(args.input_directory)
        with open(projectFile, "r") as f:
            for line in f:
                project = line.strip()
                ScoutsuiteResultsFile = Path(baseDirectory, project, "scoutsuite-results", (f"scoutsuite_results_{project}.js"))
                data = load_scoutsuite_js(ScoutsuiteResultsFile)
                storageNames = get_vulnerable_cloudstorage(data)

    
    if args.input_directory:
        baseDirectory = Path(args.input_directory)
        for directory in baseDirectory.iterdir():
            if directory.is_directory():
                ScoutsuiteResultsFile = Path(baseDirectory, directory, "scoutsuite-results", (f"scoutsuite_results_{directory}.js"))
                
    




    








if __name__ == "__main__":
    main()


