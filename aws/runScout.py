import json
import sys
#import argparse
import os
import subprocess
from pathlib import Path



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


def execScout (authType, account, creds):

    outputDir = "scoutReports" / account
    outputDir.mkdir(parents=True, exist_ok=True)
    
    if authType == "assumeRole"
        aws_access_key_id = creds["AccessKeyId"]
        aws_secret_access_key = creds["SecretAccessKey"]
        aws_session_token = creds["SessionToken"]

        scout_cmd = [
            "scout",
            "aws",
            "--report-dir",
            str(output_dir),
            "--access-keys",
            "--access-key-id",
            aws_access_key_id,
            "--secret-access-key",
            aws_secret_access_key,
            "--session-token",
            aws_session_token,
            "--max-workers",
            "6",
            "--no-browser"
        ]
    else:
        scout_cmd = [
            "scout",
            "aws",
            "--report-dir",
            str(output_dir),
            "--profile",
            account,
            "--max-workers",
            "6",
            "--no-browser"
        ]

    result = subprocess.run(scout_cmd)
    if result.returncode == 0:
        print(f"[+] Scout Suite completed for account {account}\n")
    else:
        print(f"[-] Scout Suite failed for account {account}\n")




def main():
    
    # parser = argparse.ArgumentParser(description="Parses ScoutSuite data. This script reviews the scoutsuite data and collects info on the provided cloud service(s).")
    # parser.add_argument("--input-file", help="Scoutsuite results JS file.")
    # parser.add_argument("--input-directory", help="a directory containing all of the scoutsuite projects.")
    # parser.add_argument("--account-list", help="A txt file containing a list of all AWS accounts you want checked. Helpful for splitting out data.")
    # parser.add_argument("--output-directory", help="Specify an output file to dump all of the data. Default is stdOut.")
    # parser.add_argument("--type", help="Comma separated list of services. All services will be checked if no specified. Available services are acm, awslambda, cloudformation, cloudtrail, cloudwatch, config, directconnect, ec2, efs, elasticache, elb, elbv2, emr, iam, kms, rds, redshift, route53, s3, secretsmanager, ses, sns, sqs, vpc")
    # args = parser.parse_args()


if __name__ == "__main__":
    main()


