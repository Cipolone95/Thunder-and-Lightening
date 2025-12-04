#!/usr/bin/env python3

import boto3
from pathlib import Path

aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

def list_ecs_env_vars(profile):
    
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
        client = session.client("ecs", region_name=region)

        response = client.list_task_definitions()

        task_defs = response.get("taskDefinitionArns", [])
        if not task_defs:
            print(f"[-] No Task Definitions found in region {region} ")
            continue

        for task_arn in task_defs:
                td = client.describe_task_definition(taskDefinition=task_arn)
                task_def = td["taskDefinition"]

                #print(f"Task Definition: {task_arn}")

                container_defs = task_def.get("containerDefinitions", [])

                for container in container_defs:
                    cname = container["name"]
                    env_list = container.get("environment", [])

                    #print(f"Container: {cname}")

                    if env_list:
                        writeOutputFile(f"Task Definition: {task_arn}")
                        writeOutputFile(f"Container: {cname}")
                        #print("Environment Variables:")
                        writeOutputFile("Environment Variables:")
                        for entry in env_list:
                            #print(f"{entry['name']} = {entry['value']}")
                            writeOutputFile(f"{entry['name']} = {entry['value']}")
                    # else:
                    #     print("No environment variables.")

                #print("")
                writeOutputFile("")
        
def writeOutputFile(line):
    fileName = Path(f"ECS_env_vars.txt")
    fileName.touch(exist_ok=True)
    with open(fileName, "a") as f:
        f.write(line + "\n")

def main():
    list_ecs_env_vars(None)

if __name__ == "__main__":
    main()