import boto3
import time
from botocore.exceptions import NoCredentialsError
from colorama import Fore, Style, init

def ec2_replace_root_volume(args):
    
    profile = args.profile
    region = args.region
    instance_name = args.name
    show_progress = args.show_progress
    snapshot_id = args.snapshot_id
    ami_id = args.ami_id

    # Initialize colorama
    init(autoreset=True)

    session = boto3.Session(region_name=region, profile_name=profile)
    ec2 = session.client('ec2')

    try:
        # Get instance id based on name
        response = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])
        instance_id = response['Reservations'][0]['Instances'][0]['InstanceId']

        # Specify the parameters depending on whether snapshot_id or ami_id is provided
        if snapshot_id:
            params = {"SnapshotId": snapshot_id}
        elif ami_id:
            params = {"Image": ami_id}
        else:
            print(f"{Fore.RED}You must provide either a snapshot ID or an AMI ID.{Style.RESET_ALL}")
            return

        # Create ReplaceRootVolumeTask
        task = ec2.create_replace_root_volume_task(
            InstanceId=instance_id,
            **params
        )
        task_id = task['ReplaceRootVolumeTask']['ReplaceRootVolumeTaskId']
        
        print(f"{Fore.GREEN}Created ReplaceRootVolumeTask with ID: {task_id}{Style.RESET_ALL}")

        # Progress bar
        if show_progress:
            print(f"{Fore.YELLOW}ReplaceRootVolumeTask progress:{Style.RESET_ALL}")
            while True:
                task = ec2.describe_replace_root_volume_tasks(ReplaceRootVolumeTaskIds=[task_id])
                task_status = task['ReplaceRootVolumeTasks'][0]['TaskState']
                print(f"{Fore.YELLOW}{task_status}{Style.RESET_ALL}", end='\r')
                if task_status == 'completed':
                    break
                time.sleep(5)
                
    except NoCredentialsError:
        print(f"{Fore.RED}No AWS credentials found.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
