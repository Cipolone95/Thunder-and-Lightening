import json
import re
import sys
import argparse
from pathlib import Path

import variables

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
    projects = data.get("services", {}).get(service, {}).get("projects", {})
    resourceNames = []



    for check in variables.f"{service}_checks":
        finding = findings.get(check, {})
        flagged = finding.get("flagged_items", [])

        if flagged > 0:
            print(f"[-] Cloudstorage Buckets Vulnerable to check {check}")
            bucketItems = finding.get("items",[])
            for bucketItem in bucketItems:
                bucketHash = bucketItem.split(".")[4]
                for project in projects: #will probably be some weird edge cases here at some point.
                    bucketName = projects.get(project, {}).get("buckets", {}).get(bucketHash, {}).get("name", {})
                    print(bucketName)
            print("\n")

    return list(set(open_cloudstorage_buckets))

def main():
    
    parser = argparse.ArgumentParser(description="Parses ScoutSuite data. This script reviews the scoutsuite data and collects info on the provided cloud service(s).")
    parser.add_argument("--input-file", help="Scoutsuite results JS file.")
    parser.add_argument("--input-directory", help="a directory containing all of the scoutsuite projects.")
    parser.add_argument("--project-list", help="A txt file containing a list of all projects you want checked. Helpful for splitting out data.")
    parser.add_argument("--output-file", help="Specify an output file to dump all of the data. Default is stdOut.")
    parser.add_argument("--type", help="Comma separated list of services. All services will be checked if no specified. Available services are bigquery,memorystore,cloudsql,cloudstorage,computeengine,dns,functions,iam,kms,kubernetesengine,stackdriverlogging,stackdrivermonitoring ")
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


