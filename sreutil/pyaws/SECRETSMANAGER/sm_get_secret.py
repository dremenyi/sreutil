import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from prettytable import PrettyTable
from colorama import Fore, Style, init

def sm_get_secret(args):

    # Initialize colorama
    init(autoreset=True)

    profile = args.profile
    region = args.region if args.region else 'us-gov-west-1'
    name_like = args.name_like

    session = boto3.Session(region_name=region, profile_name=profile)
    secretsmanager = session.client('secretsmanager')

    # Create PrettyTable
    table = PrettyTable()
    table.field_names = ['Path', 'Value', 'Last Updated']

    # Flag to check if any secret found
    secret_found = False

    try:
        paginator = secretsmanager.get_paginator('list_secrets')

        for page in paginator.paginate():
            for secret in page['SecretList']:
                secret_name = secret['Name']
                if name_like in secret_name:
                    try:
                        response = secretsmanager.get_secret_value(SecretId=secret_name)

                        # Get secret value
                        if 'SecretString' in response:
                            secret_value = response['SecretString']
                        else:
                            secret_value = response['SecretBinary']

                        # Get secret last updated timestamp
                        last_updated = secret['LastChangedDate']

                        # Add to the table
                        table.add_row([secret_name, secret_value, last_updated])
                        print(Fore.GREEN + f"Found secret with path {secret_name}. Adding to the table." + Style.RESET_ALL)
                        secret_found = True

                    except ClientError as e:
                        print(Fore.RED + f"Unable to retrieve secret {secret_name}" + Style.RESET_ALL)

        if not secret_found:
            print(Fore.RED + f"No secrets found with path containing '{name_like}'." + Style.RESET_ALL)
        else:
            # Print table
            print(table)

    except NoCredentialsError:
        print(Fore.RED + "No AWS credentials found." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
