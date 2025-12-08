#!/usr/bin/env python3

import boto3
from pathlib import Path

aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

def getLambdaEnvVars(profile):
    
    """
    List Lambda functions and print their names + environment variables.
    """
    # Create a session (profile optional)
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()
   
    for region in aws_regions:
        print(f"[+] Checking Region {region}")
        client = session.client("lambda", region_name=region)

        # List functions
        response = client.list_functions()

        for fn in response.get("Functions", []):
            name = fn["FunctionName"]
            env  = fn.get("Environment", {}).get("Variables", {})

            if env:
                #print(f"[+] Region {region}")
                writeOutputFile(f"[+] Region {region}",profile)
                print(f"Function: {name}")
                writeOutputFile(f"Function: {name}",profile)
                print("Environment Variables:")
                writeOutputFile("Environment Variables:",profile)
                for k, v in env.items():
                    print(f"    {k} = {v}")
                    writeOutputFile(f"{k} = {v}")
                print("")
                writeOutputFile("",profile)
            #else:
                #print("No environment variables.")
                #writeOutputFile("No environment variables.")
        

def writeOutputFile(line, profile):

    outputDirectory = Path("scoutReports" / profile)
    outputDirectory.mkdir(parents=True, exist_ok=True)

    fileName = f"Lambda_env_vars.txt"
    filepath = outputDirectory / fileName
    filepath.touch(exist_ok=True)
    with open(filePath, "a") as f:
        f.write(line + "\n")

def main():
    getLambdaEnvVars(None)

if __name__ == "__main__":
    main()