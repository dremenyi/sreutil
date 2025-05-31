import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from prettytable import PrettyTable
from colorama import Fore, Style, init
import base64

MASKED_VALUE_PLACEHOLDER = "[********]" # Should be displayed if we fetch but don't show
NOT_FETCHED_PLACEHOLDER = "[Value Not Shown]" # Should be displayed if we don't fetch

def sm_list_secrets(args):
    init(autoreset=True)

    profile = args.profile
    region = args.region
    
    # Keyword lists determination (as refined previously)
    include_keywords_default = ['jira', 'nessus', 'elk', 'kibana', 'splunk', 'palo', 'dsm', 'tower', 'ansible', 'dsm_activation_key', 'dsm_api_key']
    exclude_keywords_default = ['cert', 'key', 'index', 'token', 'cluster', 'pipeline', 'inventory', '_instance']

    current_include_keywords = include_keywords_default
    if hasattr(args, 'include_keywords') and args.include_keywords is not None:
        current_include_keywords = args.include_keywords
    
    current_exclude_keywords = exclude_keywords_default
    if hasattr(args, 'exclude_keywords') and args.exclude_keywords is not None:
        current_exclude_keywords = args.exclude_keywords

    # Simplified logic: fetch_and_show is now solely determined by args.show_values
    # The attribute 'show_values' will exist on args due to argparse definition.
    # If action='store_true', it's False if not present, True if present.
    fetch_and_show_values = args.show_values 

    session = boto3.Session(region_name=region, profile_name=profile)
    secretsmanager = session.client('secretsmanager')

    table = PrettyTable()
    table.field_names = ['Secret Name', 'Value', 'Last Changed', 'Description']
    table.align = "l"
    table.max_width["Value"] = 60
    table.max_width["Description"] = 40

    found_secrets_count = 0
    processed_secrets_for_table = 0

    try:
        print(f"{Fore.CYAN}Listing secrets in region '{region}' (Profile: {profile})...{Style.RESET_ALL}")
        if fetch_and_show_values:
            print(f"{Fore.YELLOW}WARNING: Actual secret values will be fetched and displayed! Handle with care.{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Secret values will not be fetched or shown. Use '--show-values' to display them.{Style.RESET_ALL}")

        paginator = secretsmanager.get_paginator('list_secrets')
        page_iterator = paginator.paginate()

        for page in page_iterator:
            for secret_meta in page.get('SecretList', []):
                secret_name = secret_meta['Name']
                secret_description = secret_meta.get('Description', 'N/A')
                last_changed_raw = secret_meta.get('LastChangedDate')
                last_changed_str = last_changed_raw.strftime("%Y-%m-%d %H:%M:%S %Z") if last_changed_raw else 'N/A'

                name_lower = secret_name.lower()
                if not current_include_keywords:
                    matches_include = False
                else:
                    matches_include = any(kw.lower() in name_lower for kw in current_include_keywords)
                matches_exclude = any(kw.lower() in name_lower for kw in current_exclude_keywords)

                if matches_include and not matches_exclude:
                    found_secrets_count += 1
                    secret_value_display = NOT_FETCHED_PLACEHOLDER # Default if not fetching

                    if fetch_and_show_values: # Only fetch if --show-values was used
                        print(f"{Fore.BLUE}Fetching value for matching secret: {secret_name}{Style.RESET_ALL}")
                        try:
                            secret_details = secretsmanager.get_secret_value(SecretId=secret_name)
                            
                            if 'SecretString' in secret_details:
                                secret_value_display = secret_details['SecretString']
                            elif 'SecretBinary' in secret_details:
                                try:
                                    secret_value_display = secret_details['SecretBinary'].decode('utf-8', errors='replace')
                                except: 
                                    secret_value_display = f"[Binary: {base64.b64encode(secret_details['SecretBinary']).decode('ascii')}]"
                            else:
                                secret_value_display = "[Empty Value]"

                        except ClientError as e_get_value:
                            error_code = e_get_value.response.get("Error", {}).get("Code")
                            error_message = e_get_value.response.get("Error", {}).get("Message", str(e_get_value))
                            print(f"{Fore.YELLOW}  -> Unable to retrieve value for {secret_name} ({error_code}): {error_message}{Style.RESET_ALL}")
                            secret_value_display = f"[Error: {error_code}]"
                    
                    table.add_row([secret_name, secret_value_display, last_changed_str, secret_description])
                    processed_secrets_for_table +=1
        
        if processed_secrets_for_table > 0:
            print(f"\n{Fore.GREEN}Found {found_secrets_count} secrets matching criteria. Displaying {processed_secrets_for_table} in table.{Style.RESET_ALL}")
            print(table)
            if not fetch_and_show_values and found_secrets_count > 0 : # If values were not shown but secrets were listed
                 print(f"\n{Fore.YELLOW}Secret values were not displayed. To display, use the '--show-values' flag (use with extreme caution).{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}No secrets found matching the specified filtering criteria.{Style.RESET_ALL}")

    except NoCredentialsError:
        print(f"{Fore.RED}No AWS credentials found for profile '{profile}'. Please configure.{Style.RESET_ALL}")
    except ClientError as e_list:
        error_code = e_list.response.get("Error", {}).get("Code")
        error_message = e_list.response.get("Error", {}).get("Message", str(e_list))
        print(f"{Fore.RED}AWS ClientError during 'list_secrets' (Profile: {profile}, Region: {region}): {error_message} (Code: {error_code}){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {type(e).__name__} - {e}{Style.RESET_ALL}")
