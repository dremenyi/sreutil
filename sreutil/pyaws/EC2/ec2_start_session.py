import boto3
from botocore.exceptions import ClientError, BotoCoreError
import os

def ec2_start_session(args):
    profile = args.profile
    region = args.region
    ec2_name = args.name
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')
    ssm = session.client('ssm')
    
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [ec2_name]}])

    instance_id = None

    for instance in instances:
        name_tag = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), None)
        instance_id = instance.id
        break
    if not instance_id:
        print("No instances found with the name provided.")
        return
    
    try:
        response = ssm.start_session(
            Target=instance_id,
            Reason='SSH Tunnel',
        )

        # Do something with response, like printing or opening a session via CLI
    except ClientError as e:
        print(f"Client error: {e}")
    except BotoCoreError as e:
        print(f"BotoCore error: {e}")
    
    start_session_command = f"aws ssm start-session --target {instance_id} --profile {profile} --region {region}"
    os.system(start_session_command)

    print("Successfully exited the session.")
