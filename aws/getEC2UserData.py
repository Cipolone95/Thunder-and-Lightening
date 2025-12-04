#!/usr/bin/env python3

import boto3
import base64

aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2"
]

def list_ec2_user_data(region, profile):
    
    """
    List EC2 instances in a region and print their user data (if any).
    """
    # Create a session (profile optional)
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()
   

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
                print(f"Region: {region}")
                print(f"Instance: {instance_id}")
                try:
                    user_data = base64.b64decode(user_data_b64).decode(
                        "utf-8", errors="replace"
                    )
                except Exception as e:
                    user_data = f"<error decoding user data: {e}>"

                print("User Data:")
                print(user_data)

            #print("")  # spacing
        

def main():
    for region in aws_regions:
        list_ec2_user_data(region, None)

if __name__ == "__main__":
    main()