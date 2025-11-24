#List of variables used by scoutParser.py
#Added for better readablility 


#ScoutSuite AWS Checks

act_checks = [
  # "acm-certificate-with-close-expiration-date",
  # "acm-certificate-with-transparency-logging-disabled"
]

awslambda_checks = []

cloudformation_checks = [
  # "cloudformation-stack-with-role"
]

cloudtrail_checks = [
  # "cloudtrail-duplicated-global-services-logging",
  # "cloudtrail-no-data-logging",
  # "cloudtrail-no-global-services-logging",
  # "cloudtrail-no-log-file-validation",
  # "cloudtrail-no-logging",
  # "cloudtrail-not-configured"
]

cloudwatch_checks = [
  # "cloudwatch-alarm-without-actions"
]

config_checks = [
  # "config-recorder-not-configured"
]

directconnect_checks = []

ec2_checks = [
  # "ec2-ami-public",
  # "ec2-default-security-group-in-use",
  # "ec2-default-security-group-with-rules",
  # "ec2-ebs-snapshot-not-encrypted",
  # "ec2-ebs-snapshot-public",
  # "ec2-ebs-volume-not-encrypted",
  # "ec2-instance-with-user-data-secrets",
  # "ec2-security-group-opens-DNS-port-to-all",
  # "ec2-security-group-opens-MongoDB-port-to-all",
  # "ec2-security-group-opens-MsSQL-port-to-all",
  # "ec2-security-group-opens-MySQL-port-to-all",
  # "ec2-security-group-opens-NFS-port-to-all",
  # "ec2-security-group-opens-Oracle DB-port-to-all",
  # "ec2-security-group-opens-PostgreSQL-port-to-all",
  # "ec2-security-group-opens-RDP-port-to-all",
  # "ec2-security-group-opens-SMTP-port-to-all",
  # "ec2-security-group-opens-SSH-port-to-all",
  # "ec2-security-group-opens-TCP-port-to-all",
  # "ec2-security-group-opens-UDP-port-to-all",
  # "ec2-security-group-opens-all-ports",
  # "ec2-security-group-opens-all-ports-to-all",
  # "ec2-security-group-opens-all-ports-to-self",
  # "ec2-security-group-opens-plaintext-port-FTP",
  # "ec2-security-group-opens-plaintext-port-Telnet",
  # "ec2-security-group-opens-port-range",
  # "ec2-security-group-whitelists-aws",
  # "ec2-unused-security-group"
]

efs_checks = []

elasticache_checks = []

elb_checks = [
  # "elb-no-access-logs"
]

elbv2_checks = [
  # "elbv2-no-access-logs",
  # "elbv2-no-deletion-protection",
  # "elbv2-older-ssl-policy"
]

emr_checks = []

iam_checks = [
  "iam-assume-role-lacks-external-id-and-mfa",
  "iam-assume-role-policy-allows-all",
  "iam-ec2-role-without-instances",
  "iam-group-with-inline-policies",
  "iam-group-with-no-users",
  "iam-inline-group-policy-allows-NotActions",
  "iam-inline-group-policy-allows-iam-PassRole",
  "iam-inline-group-policy-allows-sts-AssumeRole",
  "iam-inline-role-policy-allows-NotActions",
  "iam-inline-role-policy-allows-iam-PassRole",
  "iam-inline-role-policy-allows-sts-AssumeRole",
  "iam-inline-user-policy-allows-NotActions",
  "iam-inline-user-policy-allows-iam-PassRole",
  "iam-inline-user-policy-allows-sts-AssumeRole",
  "iam-managed-policy-allows-NotActions",
  "iam-managed-policy-allows-iam-PassRole",
  "iam-managed-policy-allows-sts-AssumeRole",
  "iam-managed-policy-no-attachments",
  "iam-password-policy-minimum-length",
  "iam-password-policy-no-expiration",
  "iam-password-policy-reuse-enabled",
  "iam-role-with-inline-policies",
  "iam-root-account-no-mfa",
  "iam-root-account-used-recently",
  "iam-root-account-with-active-certs",
  "iam-root-account-with-active-keys",
  "iam-user-no-Active-key-rotation",
  "iam-user-no-Inactive-key-rotation",
  "iam-user-with-inline-policies",
  "iam-user-with-multiple-access-keys",
  "iam-user-with-password-and-key",
  "iam-user-without-mfa"
]

kms_checks = []

rds_checks = [
  # "rds-instance-backup-disabled",
  # "rds-instance-ca-certificate-deprecated",
  # "rds-instance-no-minor-upgrade",
  # "rds-instance-short-backup-retention-period",
  # "rds-instance-single-az",
  # "rds-instance-storage-not-encrypted",
  # "rds-security-group-allows-all",
  # "rds-snapshot-public"
]

redshift_checks = [
  # "redshift-cluster-database-not-encrypted",
  # "redshift-cluster-no-version-upgrade",
  # "redshift-cluster-publicly-accessible",
  # "redshift-parameter-group-logging-disabled",
  # "redshift-parameter-group-ssl-not-required",
  # "redshift-security-group-whitelists-all"
]

route53_checks = [
  # "route53-domain-no-autorenew",
  # "route53-domain-no-transferlock",
  # "route53-domain-transferlock-not-authorized"
]

s3_checks = [
  #"s3-bucket-AllUsers-read",
  # "s3-bucket-AllUsers-read_acp",
  # "s3-bucket-AllUsers-write",
  # "s3-bucket-AllUsers-write_acp",
  # "s3-bucket-AuthenticatedUsers-read",
  # "s3-bucket-AuthenticatedUsers-read_acp",
  # "s3-bucket-AuthenticatedUsers-write",
  # "s3-bucket-AuthenticatedUsers-write_acp",
  "s3-bucket-allowing-cleartext",
  #"s3-bucket-no-default-encryption",
  "s3-bucket-no-logging",
  "s3-bucket-no-mfa-delete",
  "s3-bucket-no-versioning",
  #"s3-bucket-world-Delete-policy",
  #"s3-bucket-world-Get-policy",
  #"s3-bucket-world-List-policy",
  #"s3-bucket-world-Manage-policy",
  #"s3-bucket-world-Put-policy",
  #"s3-bucket-world-policy-star"
]

secretsmanager_checks = []

ses_checks = [
  # "ses-identity-dkim-not-enabled",
  # "ses-identity-dkim-not-verified",
  # "ses-identity-world-SendEmail-policy",
  # "ses-identity-world-SendRawEmail-policy"
]

sns_checks = [
  # "sns-topic-world-AddPermission-policy",
  # "sns-topic-world-DeleteTopic-policy",
  # "sns-topic-world-Publish-policy",
  # "sns-topic-world-Receive-policy",
  # "sns-topic-world-RemovePermission-policy",
  # "sns-topic-world-SetTopicAttributes-policy",
  # "sns-topic-world-Subscribe-policy"
]

sqs_checks = [
  # "sqs-queue-world-ChangeMessageVisibility-policy",
  # "sqs-queue-world-DeleteMessage-policy",
  # "sqs-queue-world-GetQueueAttributes-policy",
  # "sqs-queue-world-GetQueueUrl-policy",
  # "sqs-queue-world-PurgeQueue-policy",
  # "sqs-queue-world-ReceiveMessage-policy",
  # "sqs-queue-world-SendMessage-policy"
]

vpc_checks = [
  # "vpc-custom-network-acls-allow-all-egress",
  # "vpc-custom-network-acls-allow-all-ingress",
  # "vpc-default-network-acls-allow-all-egress",
  # "vpc-default-network-acls-allow-all-ingress",
  # "vpc-network-acl-not-used",
  # "vpc-subnet-with-allow-all-egress-acls",
  # "vpc-subnet-with-allow-all-ingress-acls",
  # "vpc-subnet-without-flow-log"
]


allServices = [
  "acm",
  "awslambda",
  "cloudformation",
  "cloudtrail",
  "cloudwatch",
  "config",
  "directconnect",
  "ec2",
  "efs",
  "elasticache",
  "elb",
  "elbv2",
  "emr",
  "iam",
  "kms",
  "rds",
  "redshift",
  "route53",
  "s3",
  "secretsmanager",
  "ses",
  "sns",
  "sqs",
  "vpc"
]

