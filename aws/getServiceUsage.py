#!/usr/bin/env python3

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# ------------------------------------------------------
#   REGIONAL SERVICES WILL LOOP ACROSS THESE REGIONS
# ------------------------------------------------------
aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]

# ------------------------------------------------------
#   SERVICE CHECK FUNCTIONS (same pattern as before)
# ------------------------------------------------------

def has_ec2(session, region):
    client = session.client("ec2", region_name=region)
    resp = client.describe_instances(MaxResults=5)
    return any(r.get("Instances") for r in resp.get("Reservations", []))

def has_lambda(session, region):
    client = session.client("lambda", region_name=region)
    resp = client.list_functions(MaxItems=5)
    return bool(resp.get("Functions"))

def has_rds(session, region):
    client = session.client("rds", region_name=region)
    resp = client.describe_db_instances(MaxRecords=5)
    return bool(resp.get("DBInstances"))

def has_ecs(session, region):
    client = session.client("ecs", region_name=region)
    resp = client.list_clusters(maxResults=5)
    return bool(resp.get("clusterArns"))

def has_eks(session, region):
    client = session.client("eks", region_name=region)
    resp = client.list_clusters(maxResults=5)
    return bool(resp.get("clusters"))

def has_sqs(session, region):
    client = session.client("sqs", region_name=region)
    resp = client.list_queues(MaxResults=5)
    return bool(resp.get("QueueUrls"))

def has_sns(session, region):
    client = session.client("sns", region_name=region)
    resp = client.list_topics()
    return bool(resp.get("Topics"))

def has_vpc(session, region):
    client = session.client("ec2", region_name=region)
    resp = client.describe_vpcs()
    return bool(resp.get("Vpcs"))

def has_elbv2(session, region):
    client = session.client("elbv2", region_name=region)
    resp = client.describe_load_balancers(PageSize=5)
    return bool(resp.get("LoadBalancers"))

def has_cloudwatch_logs(session, region):
    client = session.client("logs", region_name=region)
    resp = client.describe_log_groups(limit=5)
    return bool(resp.get("logGroups"))

def has_stepfunctions(session, region):
    client = session.client("stepfunctions", region_name=region)
    resp = client.list_state_machines(maxResults=5)
    return bool(resp.get("stateMachines"))

def has_ssm_parameters(session, region):
    client = session.client("ssm", region_name=region)
    resp = client.describe_parameters(MaxResults=5)
    return bool(resp.get("Parameters"))


# ------------------------------------------------------
#   GLOBAL SERVICE CHECK FUNCTIONS
# ------------------------------------------------------

def has_s3(session):
    client = session.client("s3")
    resp = client.list_buckets()
    return bool(resp.get("Buckets"))

def has_iam(session):
    client = session.client("iam")
    resp = client.list_roles(MaxItems=5)
    return bool(resp.get("Roles"))

def has_route53(session):
    client = session.client("route53")
    resp = client.list_hosted_zones(MaxItems="5")
    return bool(resp.get("HostedZones"))

def has_cloudtrail(session):
    client = session.client("cloudtrail")
    resp = client.describe_trails()
    return bool(resp.get("trailList"))

def has_organizations(session):
    client = session.client("organizations")
    resp = client.list_accounts(MaxResults=5)
    return bool(resp.get("Accounts"))


# ------------------------------------------------------
#   SERVICE MAPPINGS
# ------------------------------------------------------

REGIONAL_SERVICES = {
    "ec2": has_ec2,
    "lambda": has_lambda,
    "rds": has_rds,
    "ecs": has_ecs,
    "eks": has_eks,
    "sqs": has_sqs,
    "sns": has_sns,
    "vpc": has_vpc,
    "elbv2": has_elbv2,
    "cloudwatch_logs": has_cloudwatch_logs,
    "stepfunctions": has_stepfunctions,
    "ssm_parameters": has_ssm_parameters,
}

GLOBAL_SERVICES = {
    "s3": has_s3,
    "iam": has_iam,
    "route53": has_route53,
    "cloudtrail": has_cloudtrail,
    "organizations": has_organizations,
}


# ------------------------------------------------------
#   MAIN CHECK LOGIC
# ------------------------------------------------------

def check_services_in_use(profile):
    """
    Check AWS services (global + regional) for resource usage.
    """

    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()

    results = {}

    print("=== GLOBAL SERVICES ===")
    for svc, checker in GLOBAL_SERVICES.items():
        try:
            in_use = checker(session)
            results[svc] = in_use
            status = "IN USE" if in_use else "no resources found"
            print(f"  {svc}: {status}")
        except (BotoCoreError, ClientError) as e:
            print(f"  {svc}: ERROR ({e})")
            results[svc] = False

    print("\n=== REGIONAL SERVICES (US regions) ===")
    for svc, checker in REGIONAL_SERVICES.items():
        svc_in_use_any_region = False
        for region in aws_regions:
            try:
                in_use = checker(session, region)
                if in_use:
                    svc_in_use_any_region = True
                    break
            except (BotoCoreError, ClientError):
                    pass

        status = "IN USE" if svc_in_use_any_region else "no resources found"
        results[svc] = svc_in_use_any_region
        print(f"  {svc}: {status}")

    return results


def main():
    check_services_in_use(None)


if __name__ == "__main__":
    main()