import json
import re
import sys
import argparse
from pathlib import Path

import variables
import s3

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


def get_vulnerable_resources(data, service):
    findings = data.get("services", {}).get(service, {}).get("findings", {})
    #projects = data.get("services", {}).get(service, {}).get("projects", {})
    resourceNames = []



    for check in getattr(variables, f"{service}_checks"):
        finding = findings.get(check, {})
        flagged = finding.get("flagged_items", [])

        if flagged > 0:

            if check == "s3-bucket-allowing-cleartext":
                serviceObject = globals().get(service)
                method = getattr(serviceObject, "getResources")
                vulnerableResourceNames = method(data, service, check)
                for arn in vulnerableResourceNames:
                    print(arn)
            else:
                print(f"[-] {service} vulnerable to check {check}")
                vulnerableResources = finding.get("items",[])
                for resource in vulnerableResources:
                    resourceBase = resource.rsplit(".", 1)[0]
                    parts = resourceBase.split(".")
                    resourcePath = data.get("services", {})
                    for p in parts:
                        resourcePath = resourcePath.get(p, {})
                    resourceName = resourcePath.get("name", {})
                    print(resourceName)
                print("\n")

    return list(resourceNames)

def main():
    
    parser = argparse.ArgumentParser(description="Parses ScoutSuite data. This script reviews the scoutsuite data and collects info on the provided cloud service(s).")
    parser.add_argument("--input-file", help="Scoutsuite results JS file.")
    parser.add_argument("--input-directory", help="a directory containing all of the scoutsuite projects.")
    parser.add_argument("--project-list", help="A txt file containing a list of all projects you want checked. Helpful for splitting out data.")
    parser.add_argument("--output-file", help="Specify an output file to dump all of the data. Default is stdOut.")
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
            resourceNames = get_vulnerable_resources(data, service)
    
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


