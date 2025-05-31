import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from prettytable import PrettyTable
from colorama import Fore, Style, init

def sm_list_secrets(args):

    # Initialize colorama
    init(autoreset=True)

    profile = args.profile
    region = args.region if args.region else 'us-gov-west-1'

    session = boto3.Session(region_name=region, profile_name=profile)
    secretsmanager = session.client('secretsmanager')

    # List of paths to search for
    paths = ['jira', 'nessus', 'elk', 'kibana', 'splunk', 'palo', 'dsm', 'tower', 'ansible', 'dsm_activation_key', 'dsm_api_key']

    # List of paths to ignore
    ignore_paths = ['cert', 'key', 'index', 'token', 'cluster', 'pipeline', 'inventory', '_instance']

    # Create PrettyTable
    table = PrettyTable()
    table.field_names = ['Path', 'Value', 'Last Updated']

    try:
        paginator = secretsmanager.get_paginator('list_secrets')

        for page in paginator.paginate():
            for secret in page['SecretList']:
                secret_name = secret['Name']
                if any(path in secret_name for path in paths) and not any(ignore_path in secret_name for ignore_path in ignore_paths):
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

                    except ClientError as e:
                        print(Fore.RED + f"Unable to retrieve secret {secret_name}" + Style.RESET_ALL)

        # Print table
        print(table)

    except NoCredentialsError:
        print(Fore.RED + "No AWS credentials found." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
