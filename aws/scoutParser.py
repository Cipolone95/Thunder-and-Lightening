import json
import re
import sys

def load_scoutsuite_js(path):
    """
    Load ScoutSuite JS file by stripping the var assignment and parsing the JSON.
    """
    with open(path, "r") as f:
        data = f.read()

    # Remove "var scoutSuiteResults = " if present
    data = re.sub(r"scoutsuite_results\s*=", "", data.strip())
    # Remove trailing semicolon
    data = data.rstrip(";")
    
    return json.loads(data)


def get_open_s3_bucket_arns(data):
    findings = data.get("services", {}).get("s3", {}).get("findings", {})
    buckets = data.get("services", {}).get("s3", {}).get("buckets", {})
    open_bucket_arns = []

    # Common ScoutSuite finding name for public buckets
    public_keys = [
        "s3-bucket-AllUsers-read",
        "s3-bucket-AllUsers-read_acp",
        "s3-bucket-AllUsers-write",
        "s3-bucket-AllUsers-write_acp",
        "s3-bucket-AuthenticatedUsers-read",
        "s3-bucket-AuthenticatedUsers-read_acp",
        "s3-bucket-AuthenticatedUsers-write",
        "s3-bucket-AuthenticatedUsers-write_acp",
        "s3-bucket-allowing-cleartext",
        "s3-bucket-no-default-encryption",
        "s3-bucket-no-logging",
        "s3-bucket-no-mfa-delete",
        "s3-bucket-no-versioning",
        "s3-bucket-world-Delete-policy",
        "s3-bucket-world-Get-policy",
        "s3-bucket-world-List-policy",
        "s3-bucket-world-Manage-policy",
        "s3-bucket-world-Put-policy",
        "s3-bucket-world-policy-star"
    ]

    for key in public_keys:
        finding = findings.get(key, {})
        flagged = finding.get("flagged_items", [])

        if flagged > 0:
            print(f"[-] Buckets Vulnerable to check {key}")
            bucketItems = finding.get("items",[])
            for bucketItem in bucketItems:
                bucketHash = bucketItem.split(".")[2]
                bucketName = buckets.get(bucketHash, {}).get("name", {})
                print(bucketName)
            print("\n")
        #print(flagged)
        # for bucket_name in flagged:
        #     bucket = buckets.get(bucket_name, {})
        #     arn = bucket.get("arn")
        #     if arn:
        #         open_bucket_arns.append(arn)

    return list(set(open_bucket_arns))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} scoutsuite_results_aws.js")
        sys.exit(1)

    path = sys.argv[1]
    data = load_scoutsuite_js(path)
    arns = get_open_s3_bucket_arns(data)

