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


def get_vulnerable_cloudstorage(data):
    findings = data.get("services", {}).get("cloudstorage", {}).get("findings", {})
    projects = data.get("services", {}).get("cloudstorage", {}).get("projects", {})
    open_cloudstorage_buckets = []

    #GCP Bucket Checks List
    public_keys = [
        "cloudstorage-bucket-allAuthenticatedUsers",
        "cloudstorage-bucket-allUsers",
        "cloudstorage-bucket-no-logging",
        "cloudstorage-bucket-no-public-access-prevention",
        "cloudstorage-bucket-no-versioning",
        "cloudstorage-uniform-bucket-level-access-disabled"
    ]

    for key in public_keys:
        finding = findings.get(key, {})
        flagged = finding.get("flagged_items", [])

        if flagged > 0:
            print(f"[-] Cloudstorage Buckets Vulnerable to check {key}")
            bucketItems = finding.get("items",[])
            for bucketItem in bucketItems:
                bucketHash = bucketItem.split(".")[4]
                for project in projects: #will probably be some weird edge cases here at some point.
                    bucketName = projects.get(project, {}).get("buckets", {}).get(bucketHash, {}).get("name", {})
                    print(bucketName)
            print("\n")

    return list(set(open_cloudstorage_buckets))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} scoutsuite_results_gcp.js")
        sys.exit(1)

    path = sys.argv[1]
    data = load_scoutsuite_js(path)
    storageNames = get_vulnerable_cloudstorage(data)

