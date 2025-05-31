# import boto3
# import time
# from botocore.exceptions import NoCredentialsError
# from colorama import Fore, Style, init

# def ec2_create_snapshot(args):
    
#     profile = args.profile
#     region = args.region
#     instance_name = args.name
#     show_progress = args.show_progress

#     # Initialize colorama
#     init(autoreset=True)

#     session = boto3.Session(region_name=region, profile_name=profile)
#     ec2 = session.client('ec2')

#     try:
#         # Get instance id based on name
#         response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
#         instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

#         instance_info = ec2.describe_instances(InstanceIds=[instance_id])
#         root_device_name = instance_info['Reservations'][0]['Instances'][0]['RootDeviceName']
#         root_volume_id = [dev['Ebs']['VolumeId'] for dev in instance_info['Reservations'][0]['Instances'][0]['BlockDeviceMappings'] if dev['DeviceName'] == root_device_name][0]
        
#         # Create Snapshot
#         snapshot = ec2.create_snapshot(
#             Description='Created with cfAWS script',
#             VolumeId=root_volume_id
#         )
#         snapshot_id = snapshot['SnapshotId']

#         # Tag the snapshot with the instance name
#         ec2.create_tags(
#             Resources=[snapshot_id],
#             Tags=[
#                 {
#                     'Key': 'Name',
#                     'Value': instance_name
#                 },
#             ]
#         )
        
#         print(f"{Fore.GREEN}Created snapshot with ID: {snapshot_id} and tagged with Name: {instance_name}{Style.RESET_ALL}")

#         # Progress bar
#         if show_progress:
#             print(f"{Fore.YELLOW}Snapshot creation in progress. Note, Script will not be able to show actual progress\n due to aws, but it will let you know when it's completed{Style.RESET_ALL}")
#             while True:
#                 snapshot = ec2.describe_snapshots(SnapshotIds=[snapshot_id])
#                 progress = snapshot['Snapshots'][0]['Progress']
#                 print(f"{Fore.YELLOW}{progress}{Style.RESET_ALL}", end='\r')
#                 if progress == '100%':
#                     print(f"{Fore.GREEN}snapshot with ID: {snapshot_id} completed{Style.RESET_ALL}")
#                     break
#                 time.sleep(5)
                
#     except NoCredentialsError:
#         print(f"{Fore.RED}No AWS credentials found.{Style.RESET_ALL}")
#     except Exception as e:
#         print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


import boto3
import time # Keep for other uses if needed, but not for waiter polling delay
import botocore # For specific exceptions
from botocore.exceptions import NoCredentialsError, ClientError, WaiterError
from colorama import Fore, Style, init

def ec2_create_snapshot(args):
    profile = args.profile
    region = args.region
    instance_name = args.name
    show_progress = args.show_progress

    init(autoreset=True)

    session = boto3.Session(region_name=region, profile_name=profile)
    ec2 = session.client('ec2')

    try:
        print(f"{Fore.CYAN}Attempting to find instance with Name tag: {instance_name}{Style.RESET_ALL}")
        # Describe instances by Name tag
        response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])

        if not response['Reservations'] or not response['Reservations'][0]['Instances']:
            print(f"{Fore.RED}Error: No instances found with Name tag '{instance_name}'.{Style.RESET_ALL}")
            return

        if len(response['Reservations'][0]['Instances']) > 1:
            print(f"{Fore.YELLOW}Warning: Multiple instances found with Name tag '{instance_name}'. Using the first one found.{Style.RESET_ALL}")
        
        instance_data = response['Reservations'][0]['Instances'][0]
        instance_id = instance_data['InstanceId']
        print(f"{Fore.CYAN}Found instance ID: {instance_id}{Style.RESET_ALL}")

        root_device_name = instance_data.get('RootDeviceName')
        if not root_device_name:
            print(f"{Fore.RED}Error: Could not determine root device name for instance {instance_id}.{Style.RESET_ALL}")
            return

        root_volume_id = None
        for dev in instance_data.get('BlockDeviceMappings', []):
            if dev.get('DeviceName') == root_device_name:
                root_volume_id = dev.get('Ebs', {}).get('VolumeId')
                break
        
        if not root_volume_id:
            print(f"{Fore.RED}Error: Could not find EBS root volume ID for device {root_device_name} on instance {instance_id}.{Style.RESET_ALL}")
            return
        
        print(f"{Fore.CYAN}Found root volume ID: {root_volume_id} (Device: {root_device_name}){Style.RESET_ALL}")

        snapshot_description = f'Root volume snapshot for {instance_name} ({instance_id}) created by sreutil/pyaws'
        tags = [
            {'Key': 'Name', 'Value': instance_name},
            {'Key': 'sreutil:SourceInstanceId', 'Value': instance_id},
            {'Key': 'sreutil:SourceDeviceName', 'Value': root_device_name}
        ]

        print(f"{Fore.CYAN}Initiating snapshot creation for volume {root_volume_id}...{Style.RESET_ALL}")
        snapshot_response = ec2.create_snapshot(
            Description=snapshot_description,
            VolumeId=root_volume_id,
            TagSpecifications=[{'ResourceType': 'snapshot', 'Tags': tags}]
        )
        snapshot_id = snapshot_response['SnapshotId']
        
        print(f"{Fore.GREEN}Snapshot creation requested. Snapshot ID: {snapshot_id}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Tags applied: {tags}{Style.RESET_ALL}")

        if show_progress:
            print(f"{Fore.YELLOW}Waiting for snapshot {snapshot_id} to complete... (This may take several minutes){Style.RESET_ALL}")
            waiter = ec2.get_waiter('snapshot_completed')
            try:
                waiter.wait(
                    SnapshotIds=[snapshot_id],
                    WaiterConfig={'Delay': 30, 'MaxAttempts': 60} # Poll every 30s, max 30 mins
                )
                print(f"{Fore.GREEN}Snapshot {snapshot_id} completed successfully.{Style.RESET_ALL}")
            except WaiterError as e:
                # Attempt to get the last known state of the snapshot from the error
                last_state = "unknown"
                last_message = str(e)
                if e.last_response and 'Snapshots' in e.last_response and e.last_response['Snapshots']:
                    last_snapshot_details = e.last_response['Snapshots'][0]
                    last_state = last_snapshot_details.get('State', 'unknown')
                    last_message = last_snapshot_details.get('StateMessage', str(e))

                print(f"{Fore.RED}Snapshot {snapshot_id} waiter failed. Last known state: '{last_state}'. Message: {last_message}{Style.RESET_ALL}")
                print(f"{Fore.RED}Please check the AWS console for the final status of snapshot {snapshot_id}.")
        else:
            print(f"{Fore.CYAN}Snapshot creation started. To check status, use 'sreutil pyaws ec2-describe-snapshot --snapshot-id {snapshot_id} ...'{Style.RESET_ALL}")
                
    except NoCredentialsError:
        print(f"{Fore.RED}No AWS credentials found. Please configure your AWS credentials (e.g., via AWS CLI, environment variables, or IAM role).{Style.RESET_ALL}")
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        error_message = e.response.get("Error", {}).get("Message", str(e))
        print(f"{Fore.RED}AWS API Error ({error_code}): {error_message}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}An unexpected error occurred: {type(e).__name__} - {e}{Style.RESET_ALL}")
