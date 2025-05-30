import boto3
import time
from botocore.exceptions import NoCredentialsError
from colorama import Fore, Style, init

def ec2_create_snapshot(args):
    
    profile = args.profile
    region = args.region
    instance_name = args.name
    show_progress = args.show_progress

    # Initialize colorama
    init(autoreset=True)

    session = boto3.Session(region_name=region, profile_name=profile)
    ec2 = session.client('ec2')

    try:
        # Get instance id based on name
        response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
        instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

        instance_info = ec2.describe_instances(InstanceIds=[instance_id])
        root_device_name = instance_info['Reservations'][0]['Instances'][0]['RootDeviceName']
        root_volume_id = [dev['Ebs']['VolumeId'] for dev in instance_info['Reservations'][0]['Instances'][0]['BlockDeviceMappings'] if dev['DeviceName'] == root_device_name][0]
        
        # Create Snapshot
        snapshot = ec2.create_snapshot(
            Description='Created with cfAWS script',
            VolumeId=root_volume_id
        )
        snapshot_id = snapshot['SnapshotId']

        # Tag the snapshot with the instance name
        ec2.create_tags(
            Resources=[snapshot_id],
            Tags=[
                {
                    'Key': 'Name',
                    'Value': instance_name
                },
            ]
        )
        
        print(f"{Fore.GREEN}Created snapshot with ID: {snapshot_id} and tagged with Name: {instance_name}{Style.RESET_ALL}")

        # Progress bar
        if show_progress:
            print(f"{Fore.YELLOW}Snapshot creation in progress. Note, Script will not be able to show actual progress\n due to aws, but it will let you know when it's completed{Style.RESET_ALL}")
            while True:
                snapshot = ec2.describe_snapshots(SnapshotIds=[snapshot_id])
                progress = snapshot['Snapshots'][0]['Progress']
                print(f"{Fore.YELLOW}{progress}{Style.RESET_ALL}", end='\r')
                if progress == '100%':
                    print(f"{Fore.GREEN}snapshot with ID: {snapshot_id} completed{Style.RESET_ALL}")
                    break
                time.sleep(5)
                
    except NoCredentialsError:
        print(f"{Fore.RED}No AWS credentials found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

