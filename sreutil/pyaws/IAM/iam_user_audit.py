import boto3
from prettytable import PrettyTable
from datetime import datetime, timedelta
import argparse

def iam_audit(args):
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    iam = session.client('iam')

    table = PrettyTable()
    table.field_names = ["User Name", "Has MFA?", "Attached Policies", "Access Key Age (Days)", "Access Key Last Used (Days Ago)"]
    table.max_width = 30  # Set a max width for each field

    users = iam.list_users()
    for user in users['Users']:
        username = user['UserName']

        # Check for MFA
        mfa = iam.list_mfa_devices(UserName=username)
        has_mfa = "Yes" if mfa['MFADevices'] else "No"
        
        # Get attached policies
        attached_policies = []
        paginator = iam.get_paginator('list_attached_user_policies')
        for response in paginator.paginate(UserName=username):
            for policy in response['AttachedPolicies']:
                attached_policies.append(policy['PolicyName'])
        attached_policies_str = ", ".join(attached_policies)

        # Check for Access Keys
        keys = iam.list_access_keys(UserName=username)
        for key in keys['AccessKeyMetadata']:
            age = (datetime.now(key['CreateDate'].tzinfo) - key['CreateDate']).days
            last_used_response = iam.get_access_key_last_used(AccessKeyId=key['AccessKeyId'])
            if 'LastUsedDate' in last_used_response['AccessKeyLastUsed']:
                last_used = (datetime.now(last_used_response['AccessKeyLastUsed']['LastUsedDate'].tzinfo) - last_used_response['AccessKeyLastUsed']['LastUsedDate']).days
            else:
                last_used = "Never"
            table.add_row([username, has_mfa, attached_policies_str, age, last_used])

    print(table)

