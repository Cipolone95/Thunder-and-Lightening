#!/usr/bin/env python3

import argparse
import json
import os
import shutil
import subprocess
import time
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Runs different scans across multiple AWS Accounts."
    )
    parser.add_argument(
        "--profile",
        help="AWS CLI profile to use for sts assume-role",
        default=""
    )
    parser.add_argument(
        "--assume-role",
        dest="assumeRoleName",
        help="Role name to assume in each account",
        default=""
    )
    parser.add_argument(
        "--accounts",
        dest="accountFile",
        help="Path to file containing AWS account IDs (one per line)",
        required=True
    )
    parser.add_argument(
        "--sso",
        action="store_true",
        help="Enable SSO profile generation in ~/.aws/config"
    )
    parser.add_argument(
        "--sso-name",
        dest="ssoSession",
        help="Name of the SSO session to use in ~/.aws/config",
        default=""
    )
    return parser.parse_args()


def backupConfigFile(config_path: Path) -> Path:
    timestamp = int(time.time())
    backup_path = config_path.with_name(config_path.name + f".bak.{timestamp}")
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        shutil.copy2(config_path, backup_path) if config_path.exists() 
    else:
        backup_path.touch()
    
    return backup_path


def generateSSOProfiles(
    awsConfigFile: Path,
    accountFile: Path,
    sso_session,
    sso_role_name,
    sso_region,
    sso_output,
):
    # Backup config
    backupPath = backupConfigFile(awsConfigFile)
    print(f"[+] Backed up AWS config to {backupPath}")

    
    accountList = []
    with accountFile.open("r") as f:
        accountID = line.strip()
        accountList.append(accountID)

    # Append profiles to config
    with awsConfigFile.open("a", encoding="utf-8") as cfg:
        for account in accountList:
            block = (
                f"[profile {account}]\n"
                f"sso_session = {sso_session}\n"
                f"sso_account_id = {account}\n"
                f"sso_role_name = {sso_role_name}\n"
                f"region = {sso_region}\n"
                f"output = {sso_output}\n\n"
            )
            cfg.write(block)

    print(f"[+] AWS profiles have been added to {awsConfigFile}.")


def assumeRole(
    account: str,
    roleName: str,
    sessionName: str,
    profile: str
) -> dict | None:
    role_arn = f"arn:aws:iam::{account}:role/{roleName}"
    cmd = [
        "aws",
        "sts",
        "assume-role",
        "--role-arn",
        role_arn,
        "--role-session-name",
        sessionName,
        "--output",
        "json",
        "--profile",
        profile
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        stderr=subprocess.DEVNULL
    )

    if result.returncode != 0:
        print(f"❌ Failed to assume role for account {account}")
        return None

    creds_json = result.stdout
    try:
        data = json.loads(creds_json)
        return data["Credentials"]
    except (KeyError, json.JSONDecodeError) as e:
        print(f"❌ Error parsing credentials JSON for {account_id}: {e}")
        return None


def runScans(authType, account, creds):

    if authType in ("sso","profile"):
        stuff


def run_scout_for_account(
    account_id: str,
    creds: dict,
    reports_root: Path,
):
    output_dir = reports_root / account_id
    output_dir.mkdir(parents=True, exist_ok=True)

    aws_access_key_id = creds["AccessKeyId"]
    aws_secret_access_key = creds["SecretAccessKey"]
    aws_session_token = creds["SessionToken"]

    scout_cmd = [
        "scout",
        "aws",
        "--report-dir",
        str(output_dir),
        "--access-keys",
        "--access-key-id",
        aws_access_key_id,
        "--secret-access-key",
        aws_secret_access_key,
        "--session-token",
        aws_session_token,
        "--max-workers",
        "6",
        "--no-browser",
    ]

    result = subprocess.run(scout_cmd)
    if result.returncode == 0:
        print(f"✅ Scout Suite completed for account {account_id}\n")
    else:
        print(f"❌ Scout Suite failed for account {account_id}\n")


def main():
    args = parse_args()

    if args.sso and args.assume_role:
        print(f"[!] Error: Cannot specify both SSO and Assume Role.\n")
        sys.exit(1)
    
    # If SSO flag is set, generate SSO profiles in ~/.aws/config
    if args.sso:

        if not args.ssoSession:
            ssoSession = "session1"
        ssoRoleName = "AWSReadOnlyAccess"
        ssoRegion = "us-east-1"
        ssoOutput = "json"

        #Setting AWS config file  
        awsConfigFile = Path(os.path.expanduser("~")) / ".aws" / "config"

        generateSSOProfiles(
            awsConfigFile,
            accountFile,
            ssoSession,
            ssoRoleName,
            ssoRegion,
            ssoOutput
        )
    #If an assume-role name is passed in, we will authenticate using assume-role 
    elif args.assumeRoleName:
        if args.profile:
            sessionName = "ScoutSession"

            # Loop through accounts and run Scout Suite
            with accountFile.open("r", encoding="utf-8") as f:
                for line in f:
                    account = line.strip()
                    print(f"[+] Processing account: {account}")

                    roleCreds = assumeRole(
                        account_id=account,
                        role_name=assumeRoleName,
                        session_name=sessionName,
                        profile=profile,
                    )

                    if not roleCreds:
                        continue

                    runScans(authType, account, roleCreds)
        else:
            print(f"[!] Error: A profile must go with assume role. Please specify a profile.\n")
            sys.exit(1)
    else:
        #A this point only a profile was specified so that is what will be used 

if __name__ == "__main__":
    main()