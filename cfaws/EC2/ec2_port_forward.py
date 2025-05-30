import boto3
from botocore.exceptions import ClientError, BotoCoreError
import os

def ec2_port_forward(args):
    profile = args.profile
    region = args.region
    ec2_name = args.name
    port = args.port
    local_port = args.local_port
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')
    ssm = session.client('ssm')
    
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [ec2_name]}])

    instance_id = None

    for instance in instances:
        instance_id = instance.id
        break
    if not instance_id:
        print("No instances found with the name provided.")
        return

    try:
        command = f"aws ssm start-session --target {instance_id} --document-name AWS-StartPortForwardingSession --parameters 'portNumber=[\"{port}\"],localPortNumber=[\"{local_port}\"]' --profile {profile}"
        os.system(command)
        
        print("Open https://localhost:{local_port} in a browser!")
        
    except ClientError as e:
        print(f"Client error: {e}")
    except BotoCoreError as e:
        print(f"BotoCore error: {e}")
