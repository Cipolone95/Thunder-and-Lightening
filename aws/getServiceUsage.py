#!/usr/bin/env python3

import boto3
from botocore.exceptions import BotoCoreError, ClientError

# ------------------------------------------------------
#   REGIONAL SERVICES: WE LOOP THESE ACROSS aws_regions
# ------------------------------------------------------
aws_regions = [
    "us-east-1",
    "us-east-2",
    "us-west-1",
    "us-west-2",
]

# ------------------------------------------------------
#   PER-SERVICE CHECK FUNCTIONS
# ------------------------------------------------------

def has_ec2(session, region):
    client = session.client("ec2", region_name=region)
    resp = client.describe_instances(MaxResults=5)
    return any(r.get("Instances") for r in resp.get("Reservations", []))


def has_s3(session, region=None):
    # S3 treated as global here; region is ignored
    client = session.client("s3")
    resp = client.list_buckets()
    return bool(resp.get("Buckets"))


def has_rds(session, region):
    client = session.client("rds", region_name=region)
    resp = client.describe_db_instances(MaxRecords=5)
    return bool(resp.get("DBInstances"))


def has_lambda(session, region):
    client = session.client("lambda", region_name=region)
    resp = client.list_functions(MaxItems=5)
    return bool(resp.get("Functions"))


def has_ecs(session, region):
    client = session.client("ecs", region_name=region)
    resp = client.list_clusters(maxResults=5)
    return bool(resp.get("clusterArns"))


def has_eks(session, region):
    client = session.client("eks", region_name=region)
    resp = client.list_clusters(maxResults=5)
    return bool(resp.get("clusters"))


def has_ecr(session, region):
    client = session.client("ecr", region_name=region)
    resp = client.describe_repositories(maxResults=5)
    return bool(resp.get("repositories"))


def has_dynamodb(session, region):
    client = session.client("dynamodb", region_name=region)
    resp = client.list_tables(Limit=5)
    return bool(resp.get("TableNames"))


def has_sqs(session, region):
    client = session.client("sqs", region_name=region)
    resp = client.list_queues(MaxResults=5)
    return bool(resp.get("QueueUrls"))


def has_sns(session, region):
    client = session.client("sns", region_name=region)
    resp = client.list_topics()
    return bool(resp.get("Topics"))


def has_cloudwatch_alarms(session, region):
    client = session.client("cloudwatch", region_name=region)
    resp = client.describe_alarms(MaxRecords=5)
    return bool(resp.get("MetricAlarms") or resp.get("CompositeAlarms"))


def has_cloudwatch_logs(session, region):
    client = session.client("logs", region_name=region)
    resp = client.describe_log_groups(limit=5)
    return bool(resp.get("logGroups"))


def has_eventbridge(session, region):
    client = session.client("events", region_name=region)
    resp = client.list_rules(Limit=5)
    return bool(resp.get("Rules"))


def has_iam(session, region=None):
    # IAM is global; region ignored
    client = session.client("iam")
    resp = client.list_roles(MaxItems=5)
    return bool(resp.get("Roles"))


def has_kms(session, region):
    client = session.client("kms", region_name=region)
    resp = client.list_keys(Limit=5)
    return bool(resp.get("Keys"))


def has_cloudtrail(session, region=None):
    # Treat CloudTrail as global
    client = session.client("cloudtrail")
    resp = client.describe_trails()
    return bool(resp.get("trailList"))


def has_config(session, region):
    client = session.client("config", region_name=region)
    resp = client.describe_configuration_recorders()
    return bool(resp.get("ConfigurationRecorders"))


def has_guardduty(session, region):
    client = session.client("guardduty", region_name=region)
    resp = client.list_detectors()
    return bool(resp.get("DetectorIds"))


def has_securityhub(session, region):
    client = session.client("securityhub", region_name=region)
    resp = client.get_enabled_standards()
    return bool(resp.get("StandardsSubscriptions"))


def has_macie(session, region):
    client = session.client("macie2", region_name=region)
    resp = client.get_macie_session()
    return resp.get("status", "").lower() == "enabled"


def has_vpc(session, region):
    client = session.client("ec2", region_name=region)
    resp = client.describe_vpcs()
    return bool(resp.get("Vpcs"))


def has_elb(session, region):
    client = session.client("elb", region_name=region)
    resp = client.describe_load_balancers(PageSize=5)
    return bool(resp.get("LoadBalancerDescriptions"))


def has_elbv2(session, region):
    client = session.client("elbv2", region_name=region)
    resp = client.describe_load_balancers(PageSize=5)
    return bool(resp.get("LoadBalancers"))


def has_route53(session, region=None):
    # Route53 is global
    client = session.client("route53")
    resp = client.list_hosted_zones(MaxItems="5")
    return bool(resp.get("HostedZones"))


def has_acm(session, region):
    client = session.client("acm", region_name=region)
    resp = client.list_certificates(MaxItems=5)
    return bool(resp.get("CertificateSummaryList"))


def has_apigateway(session, region):
    client = session.client("apigateway", region_name=region)
    resp = client.get_rest_apis(limit=5)
    return bool(resp.get("items"))


def has_apigatewayv2(session, region):
    client = session.client("apigatewayv2", region_name=region)
    resp = client.get_apis(MaxResults="5")
    return bool(resp.get("Items"))


def has_stepfunctions(session, region):
    client = session.client("stepfunctions", region_name=region)
    resp = client.list_state_machines(maxResults=5)
    return bool(resp.get("stateMachines"))


def has_ssm(session, region):
    client = session.client("ssm", region_name=region)
    resp = client.describe_instance_information(MaxResults=5)
    return bool(resp.get("InstanceInformationList"))


def has_ssm_parameters(session, region):
    client = session.client("ssm", region_name=region)
    resp = client.describe_parameters(MaxResults=5)
    return bool(resp.get("Parameters"))


def has_backup(session, region):
    client = session.client("backup", region_name=region)
    resp = client.list_backup_vaults(MaxResults=5)
    return bool(resp.get("BackupVaultList"))


def has_organizations(session, region=None):
    # Organizations is global
    client = session.client("organizations")
    resp = client.list_accounts(MaxResults=5)
    return bool(resp.get("Accounts"))


def has_cloudformation(session, region):
    client = session.client("cloudformation", region_name=region)
    resp = client.list_stacks(MaxResults=5)
    return bool(resp.get("StackSummaries"))


def has_redshift(session, region):
    client = session.client("redshift", region_name=region)
    resp = client.describe_clusters(MaxRecords=5)
    return bool(resp.get("Clusters"))


def has_elasticache(session, region):
    client = session.client("elasticache", region_name=region)
    resp = client.describe_cache_clusters(MaxRecords=5)
    return bool(resp.get("CacheClusters"))


def has_opensearch(session, region):
    client = session.client("opensearch", region_name=region)
    resp = client.list_domain_names()
    return bool(resp.get("DomainNames"))


def has_emr(session, region):
    client = session.client("emr", region_name=region)
    resp = client.list_clusters(
        ClusterStates=["STARTING", "BOOTSTRAPPING", "RUNNING", "WAITING"]
    )
    return bool(resp.get("Clusters"))


def has_batch(session, region):
    client = session.client("batch", region_name=region)
    resp = client.describe_job_queues()
    return bool(resp.get("jobQueues"))


def has_kinesis(session, region):
    client = session.client("kinesis", region_name=region)
    resp = client.list_streams(Limit=5)
    return bool(resp.get("StreamNames"))


def has_firehose(session, region):
    client = session.client("firehose", region_name=region)
    resp = client.list_delivery_streams(Limit=5)
    return bool(resp.get("DeliveryStreamNames"))


def has_glue(session, region):
    client = session.client("glue", region_name=region)
    resp = client.get_databases(MaxResults=5)
    return bool(resp.get("DatabaseList"))


def has_athena(session, region):
    client = session.client("athena", region_name=region)
    resp = client.list_work_groups(MaxResults=5)
    return bool(resp.get("WorkGroups"))


def has_sagemaker(session, region):
    client = session.client("sagemaker", region_name=region)
    resp = client.list_notebook_instances(MaxResults=5)
    return bool(resp.get("NotebookInstances"))


def has_mq(session, region):
    client = session.client("mq", region_name=region)
    resp = client.list_brokers(MaxResults=5)
    return bool(resp.get("BrokerSummaries"))


def has_directconnect(session, region):
    client = session.client("directconnect", region_name=region)
    resp = client.describe_connections()
    return bool(resp.get("connections"))


def has_wafv2(session, region):
    client = session.client("wafv2", region_name=region)
    resp_regional = client.list_web_acls(Scope="REGIONAL", Limit=5)
    has_regional = bool(resp_regional.get("WebACLs"))
    try:
        resp_cf = client.list_web_acls(Scope="CLOUDFRONT", Limit=5)
        has_cf = bool(resp_cf.get("WebACLs"))
    except ClientError:
        has_cf = False
    return has_regional or has_cf


def has_shield(session, region=None):
    client = session.client("shield")
    resp = client.list_protections(MaxResults=5)
    return bool(resp.get("Protections"))


def has_budgets(session, region=None):
    client = session.client("budgets")
    sts = session.client("sts")
    acct = sts.get_caller_identity()["Account"]
    resp = client.describe_budgets(AccountId=acct, MaxResults=5)
    return bool(resp.get("Budgets"))


def has_cost_explorer(session, region=None):
    client = session.client("ce")
    resp = client.get_cost_and_usage(
        TimePeriod={"Start": "2024-01-01", "End": "2024-01-02"},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )
    return bool(resp.get("ResultsByTime"))

def has_cognito(session, region):
    """
    Check if Cognito User Pools exist in the region.
    """
    client = session.client("cognito-idp", region_name=region)
    resp = client.list_user_pools(MaxResults=5)
    return bool(resp.get("UserPools"))

def has_cognito_identity_pools(session, region):
    client = session.client("cognito-identity", region_name=region)
    resp = client.list_identity_pools(MaxResults=5)
    return bool(resp.get("IdentityPools"))


# ------------------------------------------------------
#   SERVICE GROUPINGS
# ------------------------------------------------------

SERVICE_CHECKS = {
    "ec2": has_ec2,
    "s3": has_s3,
    "rds": has_rds,
    "lambda": has_lambda,
    "ecs": has_ecs,
    "eks": has_eks,
    "ecr": has_ecr,
    "dynamodb": has_dynamodb,
    "sqs": has_sqs,
    "sns": has_sns,
    "cloudwatch_alarms": has_cloudwatch_alarms,
    "cloudwatch_logs": has_cloudwatch_logs,
    "eventbridge": has_eventbridge,
    "iam": has_iam,
    "kms": has_kms,
    "cloudtrail": has_cloudtrail,
    "config": has_config,
    "guardduty": has_guardduty,
    "securityhub": has_securityhub,
    "macie": has_macie,
    "vpc": has_vpc,
    "elb": has_elb,
    "elbv2": has_elbv2,
    "route53": has_route53,
    "acm": has_acm,
    "apigateway": has_apigateway,
    "apigatewayv2": has_apigatewayv2,
    "stepfunctions": has_stepfunctions,
    "ssm_managed_instances": has_ssm,
    "ssm_parameters": has_ssm_parameters,
    "backup": has_backup,
    "organizations": has_organizations,
    "cloudformation": has_cloudformation,
    "redshift": has_redshift,
    "elasticache": has_elasticache,
    "opensearch": has_opensearch,
    "emr": has_emr,
    "batch": has_batch,
    "kinesis": has_kinesis,
    "firehose": has_firehose,
    "glue": has_glue,
    "athena": has_athena,
    "sagemaker": has_sagemaker,
    "mq": has_mq,
    "directconnect": has_directconnect,
    "wafv2": has_wafv2,
    "shield": has_shield,
    "budgets": has_budgets,
    "cost_explorer": has_cost_explorer,
    "cognito": has_cognito,                
    "cognito_identity_pools": has_cognito_identity_pools
}

GLOBAL_SERVICES = {
    "s3": has_s3,
    "iam": has_iam,
    "cloudtrail": has_cloudtrail,
    "route53": has_route53,
    "organizations": has_organizations,
    "shield": has_shield,
    "budgets": has_budgets,
    "cost_explorer": has_cost_explorer,
}

REGIONAL_SERVICES = {
    "ec2": has_ec2,
    "rds": has_rds,
    "lambda": has_lambda,
    "ecs": has_ecs,
    "eks": has_eks,
    "ecr": has_ecr,
    "dynamodb": has_dynamodb,
    "sqs": has_sqs,
    "sns": has_sns,
    "cloudwatch_alarms": has_cloudwatch_alarms,
    "cloudwatch_logs": has_cloudwatch_logs,
    "eventbridge": has_eventbridge,
    "kms": has_kms,
    "config": has_config,
    "guardduty": has_guardduty,
    "securityhub": has_securityhub,
    "macie": has_macie,
    "vpc": has_vpc,
    "elb": has_elb,
    "elbv2": has_elbv2,
    "acm": has_acm,
    "apigateway": has_apigateway,
    "apigatewayv2": has_apigatewayv2,
    "stepfunctions": has_stepfunctions,
    "ssm_managed_instances": has_ssm,
    "ssm_parameters": has_ssm_parameters,
    "backup": has_backup,
    "cloudformation": has_cloudformation,
    "redshift": has_redshift,
    "elasticache": has_elasticache,
    "opensearch": has_opensearch,
    "emr": has_emr,
    "batch": has_batch,
    "kinesis": has_kinesis,
    "firehose": has_firehose,
    "glue": has_glue,
    "athena": has_athena,
    "sagemaker": has_sagemaker,
    "mq": has_mq,
    "directconnect": has_directconnect,
    "wafv2": has_wafv2,
}

# ------------------------------------------------------
#   MAIN CHECKING LOGIC (WITH PER-REGION OUTPUT)
# ------------------------------------------------------

def check_services_in_use(profile=None):
    """
    Check many AWS services and report whether they have any resources.

    Returns:
        {
          "global": { service_name: bool, ... },
          "regional": { service_name: { region: bool, ... }, ... }
        }
    """
    if profile:
        session = boto3.Session(profile_name=profile)
    else:
        session = boto3.Session()

    results = {
        "global": {},
        "regional": {},
    }

    print("=== GLOBAL SERVICES ===")
    for svc, checker in GLOBAL_SERVICES.items():
        try:
            in_use = checker(session)
            results["global"][svc] = in_use
            status = "IN USE" if in_use else "no resources found"
            print(f"  {svc}: {status}")
        except (BotoCoreError, ClientError) as e:
            print(f"  {svc}: ERROR ({e})")
            results["global"][svc] = False

    print("\n=== REGIONAL SERVICES (US regions) ===")
    for svc, checker in REGIONAL_SERVICES.items():
        svc_region_results = {}
        svc_in_use_any_region = False

        print(f"\n  {svc}:")
        for region in aws_regions:
            try:
                in_use = checker(session, region)
            except (BotoCoreError, ClientError):
                in_use = False

            svc_region_results[region] = in_use
            if in_use:
                svc_in_use_any_region = True

            # Per-region line
            region_status = "IN USE" if in_use else "no resources found"
            print(f"    {region}: {region_status}")

        results["regional"][svc] = svc_region_results

    return results


def main():
    # Edit profile name as needed, or keep None for default env/instance creds
    check_services_in_use(profile=None)


if __name__ == "__main__":
    main()