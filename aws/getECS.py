#!/usr/bin/env python3

import boto3

aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

def list_ecs_env_vars(region, profile):
    
    """
    List Lambda functions and print their names + environment variables.
    """
    # Create a session (profile optional)
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()
   

    client = session.client("ecs", region_name=region)

    # List functions
    response = client.list_task_definitions()

    task_defs = response.get("taskDefinitionArns", [])
    if not task_defs:
        print(f"[-] No Task Definitions found in region {region} ")

    for task_arn in task_defs:
            td = client.describe_task_definition(taskDefinition=task_arn)
            task_def = td["taskDefinition"]

            print(f"Task Definition: {task_arn}")

            container_defs = task_def.get("containerDefinitions", [])

            for container in container_defs:
                cname = container["name"]
                env_list = container.get("environment", [])

                print(f"  Container: {cname}")

                if env_list:
                    print("    Environment Variables:")
                    for entry in env_list:
                        print(f"      {entry['name']} = {entry['value']}")
                else:
                    print("    No environment variables.")

            print("")
        

def main():
    for region in aws_regions:
        list_ecs_env_vars(region, None)

if __name__ == "__main__":
    main()