#!/usr/bin/env python3

import boto3

aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

def list_lambda_functions(region, profile):
    
    """
    List Lambda functions and print their names + environment variables.
    """
    # Create a session (profile optional)
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()
   

    client = session.client("lambda", region_name=region)

    # List functions
    response = client.list_functions()

    for fn in response.get("Functions", []):
        name = fn["FunctionName"]
        env  = fn.get("Environment", {}).get("Variables", {})

        if env:
            print(f"[+] Region {region}")
            print(f"Function: {name}")
            print("  Environment Variables:")
            for k, v in env.items():
                print(f"    {k} = {v}")
            print("")
        # else:
        #     print("  No environment variables.")
        

def main():
    for region in aws_regions:
        list_lambda_functions(region, None)

if __name__ == "__main__":
    main()