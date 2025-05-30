import boto3
import argparse
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from colorama import Fore, Style

def iam_rotate_key(args):
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    iam = session.client('iam')

    # Get the keys for the user
    access_keys = iam.list_access_keys(UserName=args.user)['AccessKeyMetadata']

    if len(access_keys) < 1:
        print(Fore.RED + "No active keys found for this user." + Style.RESET_ALL)

    # Ask if the user wants to create a key or deactivate one
    print(Fore.YELLOW + "Would you like to:\n1. Deactivate a key\n2. Create a new key" + Style.RESET_ALL)
    choice = int(input("Enter your choice (1 or 2):"))
    if choice == 1:
        if len(access_keys) < 1:
            print(Fore.RED + "No active keys to deactivate." + Style.RESET_ALL)
            return
        for key in access_keys:
            key_age = relativedelta(datetime.now(timezone.utc), key['CreateDate']).years * 365 + \
                       relativedelta(datetime.now(timezone.utc), key['CreateDate']).months * 30 + \
                       relativedelta(datetime.now(timezone.utc), key['CreateDate']).days
            print(Fore.YELLOW + f"Key: {key['AccessKeyId']}, Age: {key_age} days" + Style.RESET_ALL)
        key_choice = input("Enter the key ID to be deactivated:")
        iam.update_access_key(UserName=args.user, AccessKeyId=key_choice, Status='Inactive')
        iam.delete_access_key(UserName=args.user, AccessKeyId=key_choice)
        print(Fore.GREEN + f"Access key {key_choice} deactivated and deleted." + Style.RESET_ALL)
    elif choice == 2:
        if len(access_keys) >= 2:
            print(Fore.RED + "User already has two active keys. Deactivate a key first." + Style.RESET_ALL)
            return
        # Create a new access key
        new_key = iam.create_access_key(UserName=args.user)['AccessKey']
        print(Fore.GREEN + f"New Access Key created! Access Key ID: {new_key['AccessKeyId']}, Secret Access Key: {new_key['SecretAccessKey']}" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
