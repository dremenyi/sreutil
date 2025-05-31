import boto3
from prettytable import PrettyTable
import csv # Import the CSV module
from botocore.exceptions import NoCredentialsError, ClientError
from colorama import Fore, Style, init

def ec2_inventory(args):
    profile = args.profile
    region = args.region
    output_file_path = args.output

    init(autoreset=True)

    print(f"{Fore.CYAN}Attempting to gather EC2 inventory for region '{region}' using profile '{profile}'...{Style.RESET_ALL}")

    try:
        session = boto3.Session(profile_name=profile, region_name=region)
        ec2_resource = session.resource('ec2')
        ec2_client = session.client('ec2')

        print(f"{Fore.CYAN}Fetching all subnet details...{Style.RESET_ALL}")
        all_subnets_response = ec2_client.describe_subnets()
        subnet_name_map = {}
        for subnet_detail in all_subnets_response.get('Subnets', []):
            s_name = ''
            for tag in subnet_detail.get('Tags', []):
                if tag['Key'] == 'Name':
                    s_name = tag['Value']
                    break
            subnet_name_map[subnet_detail['SubnetId']] = s_name
        print(f"{Fore.CYAN}Found {len(subnet_name_map)} subnets.{Style.RESET_ALL}")

        # Define field names for both PrettyTable and CSV header
        field_names = ["Instance ID", "Name Tag", "Instance State", "Instance Type", 
                       "Public IP", "Private IP", "Subnet ID", "Subnet Name", "VPC ID"]
        
        table = PrettyTable()
        table.field_names = field_names
        table.align = "l"

        # Prepare data rows for both PrettyTable and CSV
        data_for_output = []

        print(f"{Fore.CYAN}Fetching instance details... (this might take a moment for many instances){Style.RESET_ALL}")
        instance_count = 0
        for instance in ec2_resource.instances.all():
            instance_count += 1
            name_tag = ''
            if instance.tags:
                for tag in instance.tags:
                    if tag['Key'] == 'Name':
                        name_tag = tag['Value']
                        break

            subnet_id_str = instance.subnet_id if instance.subnet_id else 'N/A'
            current_subnet_name = subnet_name_map.get(instance.subnet_id, '') if instance.subnet_id else ''
            vpc_id_str = instance.vpc_id if instance.vpc_id else 'N/A'

            row_data = [
                instance.id,
                name_tag,
                instance.state['Name'] if instance.state else 'N/A',
                instance.instance_type,
                instance.public_ip_address if instance.public_ip_address else 'N/A',
                instance.private_ip_address if instance.private_ip_address else 'N/A',
                subnet_id_str,
                current_subnet_name,
                vpc_id_str
            ]
            table.add_row(row_data) # Add to PrettyTable
            data_for_output.append(row_data) # Add to list for CSV

        print(f"{Fore.GREEN}Processed {instance_count} instances.{Style.RESET_ALL}")

        if output_file_path:
            try:
                with open(output_file_path, 'w', newline='') as csvfile: # Open with newline='' for csv
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow(field_names) # Write header row
                    csv_writer.writerows(data_for_output) # Write all data rows
                print(f"{Fore.GREEN}Inventory data successfully written to CSV file: {output_file_path}{Style.RESET_ALL}")
            except IOError as e:
                print(f"{Fore.RED}Error writing to CSV file {output_file_path}: {e}{Style.RESET_ALL}")
        else:
            print(table) # Print PrettyTable to console if no output file

    except NoCredentialsError:
        print(f"{Fore.RED}No AWS credentials found for profile '{profile}'. Please configure your AWS credentials.{Style.RESET_ALL}")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        if "AuthFailure" in error_code or "OptInRequired" in error_code:
             print(f"{Fore.RED}AWS Authentication/Authorization Error for profile '{profile}' in region '{region}': {error_message}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}AWS ClientError in region '{region}' (Profile: {profile}): {error_message} (Code: {error_code}){Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {type(e).__name__} - {e}{Style.RESET_ALL}")

