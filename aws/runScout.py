import argparse
import subprocess
from pathlib import Path

def execScout (authType, account, creds, outputDirectory):

    if not outputDirectory:
        outputDirectory = Path("output") / account / "scoutFiles"
        outputDirectory.mkdir(parents=True, exist_ok=True)
    else:
        Path(outputDirectory)
        outputDirectory.mkdir(parents=True, exist_ok=True)
    
    if authType == "assumeRole":
        aws_access_key_id = creds["AccessKeyId"]
        aws_secret_access_key = creds["SecretAccessKey"]
        aws_session_token = creds["SessionToken"]

        scout_cmd = [
            "scout",
            "aws",
            "--report-dir",
            str(outputDirectory),
            "--access-keys",
            "--access-key-id",
            aws_access_key_id,
            "--secret-access-key",
            aws_secret_access_key,
            "--session-token",
            aws_session_token,
            "--max-workers",
            "6",
            "--no-browser"
        ]
    else:
        scout_cmd = [
            "scout",
            "aws",
            "--report-dir",
            str(outputDirectory),
            "--profile",
            account,
            "--max-workers",
            "6",
            "--no-browser"
        ]

    result = subprocess.run(scout_cmd)
    if result.returncode == 0:
        print(f"[+] Scout Suite completed for account {account}\n")
    else:
        print(f"[-] Scout Suite failed for account {account}\n")


def main():
    
    parser = argparse.ArgumentParser(description="Parses ScoutSuite data. This script reviews the scoutsuite data and collects info on the provided cloud service(s).")
    parser.add_argument("--account-list", help="""A txt file containing a list of all AWS accounts you want checked. 
    Note: Profiles will need to be made with AWS account number as profile name""")
    parser.add_argument("--output-directory", help="Specify an output file to dump all of the data")
    args = parser.parse_args()

    
    with args.account_list.open("r", encoding="utf-8") as f:
        for line in f:
            account = line.strip()
            print(f"[+] Processing account: {account}")
            execScout("profile", account, None, args.output_directory)
    
    

if __name__ == "__main__":
    main()


