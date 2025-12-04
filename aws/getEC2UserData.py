#!/usr/bin/env python3

import boto3
import base64
from pathlib import Path

aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

def list_ec2_user_data(profile):
    
    """
    List EC2 instances in a region and print their user data (if any).
    """
    # Create a session (profile optional)
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()
   
    for region in aws_regions:
        client = session.client("ec2", region_name=region)

        response = client.describe_instances()

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance["InstanceId"]

                # Get the user data attribute for this instance
                attr = client.describe_instance_attribute(
                    InstanceId=instance_id,
                    Attribute="userData",
                )

                user_data_b64 = attr.get("UserData", {}).get("Value")

                

                if user_data_b64:
                    #print(f"Region: {region}")
                    #print(f"Instance: {instance_id}")
                    writeOutputFile(f"Region: {region}")
                    writeOutputFile(f"Instance: {instance_id}")
                    try:
                        user_data = base64.b64decode(user_data_b64).decode(
                            "utf-8", errors="replace"
                        )
                    except Exception as e:
                        user_data = f"<error decoding user data: {e}>"

                    #print("User Data:")
                    #print(user_data)
                    writeOutputFile("User Data:")
                    writeOutputFile(user_data)

                #print("")  # spacing
        
def writeOutputFile(line):
    fileName = Path(f"EC2_userData.txt")
    fileName.touch(exist_ok=True)
    with open(fileName, "a") as f:
        f.write(line + "\n")

def main():
    list_ec2_user_data(None)

if __name__ == "__main__":
    main()