#List of variables used by scoutParser.py
#Added for better readablility 


#ScoutSuite GCP Checks
bigquery_checks = [
  "bigquery-dataset-allAuthenticatedUsers",
  "bigquery-dataset-allUsers",
  "bigquery-encryption-no-cmk"
]

cloudmemorystore_checks = [
  "memorystore-redis-instance-auth-not-enabled",
  "memorystore-redis-instance-ssl-not-required"
]

cloudsql_checks = [
  "cloudsql-allows-root-login-from-any-host",
  "cloudsql-instance-backups-disabled",
  "cloudsql-instance-is-open-to-public-range",
  "cloudsql-instance-is-open-to-the-world",
  "cloudsql-instance-no-binary-logging",
  "cloudsql-instance-ssl-not-required",
  "cloudsql-instance-with-no-backups",
  "cloudsql-instances-public-ips",
  "cloudsql-mysql-instances-local-infile-on",
  "cloudsql-postgresql-instances-log-checkpoints-off",
  "cloudsql-postgresql-instances-log-connections-off",
  "cloudsql-postgresql-instances-log-disconnections-off",
  "cloudsql-postgresql-instances-log-lock-waits-off",
  "cloudsql-postgresql-instances-log-min-duration-not-set-1",
  "cloudsql-postgresql-instances-log-min-messages-not-set",
  "cloudsql-postgresql-instances-log-temp-files-not-set-0",
  "cloudsql-sqlservers-instances-contained-database-authentication-on",
  "cloudsql-sqlservers-instances-cross-db-ownership-chaining-on"
]

  
cloudstorage_checks = [
    "cloudstorage-bucket-allAuthenticatedUsers",
    "cloudstorage-bucket-allUsers",
    "cloudstorage-bucket-no-logging",
    "cloudstorage-bucket-no-public-access-prevention",
    "cloudstorage-bucket-no-versioning",
    "cloudstorage-uniform-bucket-level-access-disabled"
]

computeengine_checks = [
  "computeengine-firewall-default-rule-in-use",
  #"computeengine-firewall-rule-allows-all-ports",
  #"computeengine-firewall-rule-allows-internal-traffic",
  #"computeengine-firewall-rule-allows-port-range",
  #"computeengine-firewall-rule-allows-public-access",
  #"computeengine-firewall-rule-opens-all-ports-to-all",
  #"computeengine-firewall-rule-opens-sensitive-port-to-all",
  "computeengine-instance-block-project-ssh-keys-disabled",
  "computeengine-instance-connecting-serial-ports-enabled",
  "computeengine-instance-default-service-account",
  #"computeengine-instance-disk-not-csek-encrypted",
  #"computeengine-instance-disk-with-no-snapshot",
  "computeengine-instance-full-api-access",
  "computeengine-instance-ip-forwarding-enabled",
  "computeengine-instance-os-login-disabled",
  "computeengine-instance-public-ip-adresses",
  "computeengine-instance-shielded-vm-disabled",
  "computeengine-instance-with-deletion-protection-disabled",
  #"computeengine-loadbalancer-forwarding-rule-forwards-sensitive-port",
  "computeengine-loadbalancer-global-forwarding-rule-forwards-sensitive-port",
  #"computeengine-network-default-in-use",
  "computeengine-network-legacy-in-use",
  "computeengine-network-with-no-instances",
  "computeengine-old-disk-snapshot",
  "computeengine-vpc-flow-logs-disabled"
]

dns_checks = [
  "dns-zones-dnssec-not-enabled",
  "dns-zones-key-signing-key-using-rsasha1",
  "dns-zones-zone-signing-key-using-rsasha1"
]

functions_checks = [
  "functions-v1-allowing-http",
  "functions-v1-environment-variables-secrets",
  "functions-v1-function-allAuthenticatedUsers",
  "functions-v1-function-allUsers",
  "functions-v1-public-endpoint",
  "functions-v2-environment-variables-secrets",
  "functions-v2-public-endpoint"
]

iam_checks = [
  "iam-gmail-accounts-used",
  "iam-lack-of-service-account-key-rotation",
  "iam-primitive-role-in-use",
  "iam-role-account-separation-duties-is-false",
  "iam-role-assigned-to-domain",
  "iam-role-assigned-to-user",
  "iam-role-kms-separation-duties-is-false",
  "iam-sa-has-admin-privileges",
  "iam-service-account-user-allAuthenticatedUsers",
  "iam-service-account-user-allUsers",
  "iam-service-account-with-user-managed-keys",
  "iam-user-has-sa-user-role"
]

kms_checks = [
  "kms-cryptokeys-anonymously-publicly-accessible",
  "kms-encryption-keys-not-rotated"
]

kubernetesengine_checks = [
  "kubernetesengine-basic-authentication-enabled",
  "kubernetesengine-certificate-authentication-enabled",
  "kubernetesengine-cluster-alias-ip-disabled",
  "kubernetesengine-cluster-application-layer-encryption-disabled",
  "kubernetesengine-cluster-binary-authorization-disabled",
  "kubernetesengine-cluster-has-no-labels",
  "kubernetesengine-cluster-logging-disabled",
  "kubernetesengine-cluster-master-authorized-networks-disabled",
  "kubernetesengine-cluster-metadata-server-disabled",
  "kubernetesengine-cluster-monitoring-disabled",
  "kubernetesengine-cluster-network-policy-disabled",
  "kubernetesengine-cluster-pod-security-policy-config-disabled",
  "kubernetesengine-cluster-private-endpoint-disabled",
  "kubernetesengine-cluster-private-google-access-disabled",
  "kubernetesengine-cluster-release-channel",
  "kubernetesengine-cluster-shielded-nodes-disabled",
  "kubernetesengine-cluster-workload-identity-disabled",
  "kubernetesengine-dashboard-enabled",
  "kubernetesengine-default-service-account-used",
  "kubernetesengine-legacy-abac-enabled",
  "kubernetesengine-legacy-metadata-endpoints-enabled",
  "kubernetesengine-node-auto-repair-disabled",
  "kubernetesengine-node-auto-upgrade-disabled",
  "kubernetesengine-node-container-optimized-os-not-used",
  "kubernetesengine-node-integrity-monitoring-disabled",
  "kubernetesengine-node-secure-boot-disabled",
  "kubernetesengine-private-nodes-disabled",
  "kubernetesengine-scopes-not-limited"
]

stackdriverlogging_checks = [
  "stackdriverlogging-metric-filter-does-not-exist-audit-config-changes",
  "stackdriverlogging-metric-filter-does-not-exist-cloud-storage-iam-permission-changes",
  "stackdriverlogging-metric-filter-does-not-exist-custom-role-changes",
  "stackdriverlogging-metric-filter-does-not-exist-project-ownership-assignment",
  "stackdriverlogging-metric-filter-does-not-exist-sql-instance-config-changes",
  "stackdriverlogging-metric-filter-does-not-exist-vpc-network-changes",
  "stackdriverlogging-metric-filter-does-not-exist-vpc-network-firewall-rule-changes",
  "stackdriverlogging-metric-filter-does-not-exist-vpc-network-route-changes",
  "stackdriverlogging-no-export-sinks"
]

stackdrivermonitoring_checks = [
  "stackdrivermonitoring-alerts-does-not-exist-audit-config-changes",
  "stackdrivermonitoring-alerts-does-not-exist-cloud-storage-iam-permission-changes",
  "stackdrivermonitoring-alerts-does-not-exist-custom-role-changes",
  "stackdrivermonitoring-alerts-does-not-exist-project-ownership-assignment",
  "stackdrivermonitoring-alerts-does-not-exist-sql-instance-config-changes",
  "stackdrivermonitoring-alerts-does-not-exist-vpc-network-changes",
  "stackdrivermonitoring-alerts-does-not-exist-vpc-network-firewall-rule-changes",
  "stackdrivermonitoring-alerts-does-not-exist-vpc-network-route-changes"
]

allServices = [
    "bigquery",
    "memorystore",
    "cloudsql",
    "cloudstorage",
    "computeengine",
    "dns",
    "functions",
    "iam",
    "kms",
    "kubernetesengine",
    "stackdriverlogging",
    "stackdrivermonitoring",
]

