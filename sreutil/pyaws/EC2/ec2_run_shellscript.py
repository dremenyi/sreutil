import boto3
import argparse
import time
import os

def get_linux_instances(client):
    response = client.describe_instances(
        Filters=[
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            platform_details = instance.get('PlatformDetails', 'Linux/UNIX')
            if 'Linux' in platform_details:
                instances.append(instance['InstanceId'])
    return instances

def get_instance_ids_by_names(client, names):
    response = client.describe_instances(
        Filters=[
            {'Name': 'tag:Name', 'Values': names},
            {'Name': 'instance-state-name', 'Values': ['running']}
        ]
    )
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            platform_details = instance.get('PlatformDetails', 'Linux/UNIX')
            if 'Linux' in platform_details:
                instances.append(instance['InstanceId'])
    return instances

def filter_valid_instances(instance_ids, region='us-east-1'):
    ssm_client = boto3.client('ssm', region_name=region)
    response = ssm_client.describe_instance_information()
    valid_instances = [instance['InstanceId'] for instance in response['InstanceInformationList']]
    return [instance_id for instance_id in instance_ids if instance_id in valid_instances]

def run_shell_script(instance_ids, script, region='us-east-1'):
    ssm_client = boto3.client('ssm', region_name=region)
    response = ssm_client.send_command(
        InstanceIds=instance_ids,
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': [script]},
    )
    command_id = response['Command']['CommandId']
    return command_id

def get_command_output(instance_ids, command_id, region='us-east-1', max_retries=30, delay=10):
    ssm_client = boto3.client('ssm', region_name=region)
    output = {}
    for instance_id in instance_ids:
        output[instance_id] = {}
        retries = 0
        while retries < max_retries:
            try:
                response = ssm_client.get_command_invocation(
                    CommandId=command_id,
                    InstanceId=instance_id
                )
                status = response['Status']
                if status in ['Success', 'Failed']:
                    output[instance_id]['Status'] = status
                    output[instance_id]['Output'] = response['StandardOutputContent']
                    output[instance_id]['Error'] = response['StandardErrorContent']
                    break
                else:
                    print(f"Command status for instance {instance_id} is {status}. Retrying...")
                    time.sleep(delay)
                    retries += 1
            except ssm_client.exceptions.InvocationDoesNotExist:
                print(f"Invocation does not exist for instance {instance_id}. Retrying...")
                time.sleep(delay)
                retries += 1
    return output

def ec2_run_shellscript(args):
    if not args.all_linux_instances and not args.targets:
        print('You must specify --all-linux-instances or provide instance names with --targets.')
        return

    if not os.path.isfile(args.file):
        print(f'The file {args.file} does not exist.')
        return

    with open(args.file, 'r') as file:
        script = file.read()

    ec2_client = boto3.client('ec2', region_name=args.region)

    if args.all_linux_instances:
        print("Fetching all Linux instances...")
        instance_ids = get_linux_instances(ec2_client)
        print(f"Found instances: {instance_ids}")
    else:
        print("Fetching instances by name...")
        instance_ids = get_instance_ids_by_names(ec2_client, args.targets)
        print(f"Found instances: {instance_ids}")

    valid_instance_ids = filter_valid_instances(instance_ids, args.region)
    if not valid_instance_ids:
        print("No valid instances found. Exiting.")
        return

    print(f"Targeting valid instances: {valid_instance_ids}")
    command_id = run_shell_script(valid_instance_ids, script, args.region)
    print(f"Command ID: {command_id}")

    output = get_command_output(valid_instance_ids, command_id, args.region)
    print("Command output:")

    for instance_id, result in output.items():
        print(f"Instance ID: {instance_id}")
        print(f"Status: {result['Status']}")
        print(f"Output: {result['Output']}")
        print(f"Error: {result['Error']}")
        print('-' * 60)

# import boto3
# import argparse
# import time
# import os

# def get_linux_instances(client):
#     response = client.describe_instances(
#         Filters=[
#             {'Name': 'instance-state-name', 'Values': ['running']}
#         ]
#     )
#     instances = []
#     for reservation in response['Reservations']:
#         for instance in reservation['Instances']:
#             platform_details = instance.get('PlatformDetails', 'Linux/UNIX')
#             if 'Linux' in platform_details:
#                 instances.append(instance['InstanceId'])
#     return instances

# def get_instance_ids_by_names(client, names):
#     response = client.describe_instances(
#         Filters=[
#             {'Name': 'tag:Name', 'Values': names},
#             {'Name': 'instance-state-name', 'Values': ['running']}
#         ]
#     )
#     instances = []
#     for reservation in response['Reservations']:
#         for instance in reservation['Instances']:
#             platform_details = instance.get('PlatformDetails', 'Linux/UNIX')
#             if 'Linux' in platform_details:
#                 instances.append(instance['InstanceId'])
#     return instances

# def filter_valid_instances(instance_ids, region='us-east-1'):
#     ssm_client = boto3.client('ssm', region_name=region)
#     response = ssm_client.describe_instance_information()
#     valid_instances = [instance['InstanceId'] for instance in response['InstanceInformationList']]
#     return [instance_id for instance_id in instance_ids if instance_id in valid_instances]

# def run_shell_script(instance_ids, script, region='us-east-1'):
#     ssm_client = boto3.client('ssm', region_name=region)
#     response = ssm_client.send_command(
#         InstanceIds=instance_ids,
#         DocumentName='AWS-RunShellScript',
#         Parameters={'commands': [script]},
#     )
#     command_id = response['Command']['CommandId']
#     return command_id

# def get_command_output(instance_ids, command_id, region='us-east-1', max_retries=30, delay=10):
#     ssm_client = boto3.client('ssm', region_name=region)
#     output = {}
#     for instance_id in instance_ids:
#         output[instance_id] = {}
#         retries = 0
#         while retries < max_retries:
#             try:
#                 response = ssm_client.get_command_invocation(
#                     CommandId=command_id,
#                     InstanceId=instance_id
#                 )
#                 status = response['Status']
#                 if status in ['Success', 'Failed']:
#                     output[instance_id]['Status'] = status
#                     output[instance_id]['Output'] = response['StandardOutputContent']
#                     output[instance_id]['Error'] = response['StandardErrorContent']
#                     break
#                 else:
#                     print(f"Command status for instance {instance_id} is {status}. Retrying...")
#                     time.sleep(delay)
#                     retries += 1
#             except ssm_client.exceptions.InvocationDoesNotExist:
#                 print(f"Invocation does not exist for instance {instance_id}. Retrying...")
#                 time.sleep(delay)
#                 retries += 1
#     return output

# def ec2_run_shellscript(args):
#     script_file = args.file
#     bash_directory = os.path.join(os.path.dirname(__file__), '..', 'bash')

#     if not os.path.isabs(script_file):
#         script_file = os.path.join(bash_directory, script_file)

#     if not os.path.isfile(script_file):
#         print(f'The file {script_file} does not exist.')
#         return

#     with open(script_file, 'r') as file:
#         script = file.read()

#     ec2_client = boto3.client('ec2', region_name='us-east-1')

#     if args.all_linux_instances:
#         print("Fetching all Linux instances...")
#         instance_ids = get_linux_instances(ec2_client)
#         print(f"Found instances: {instance_ids}")
#     else:
#         print("Fetching instances by name...")
#         instance_ids = get_instance_ids_by_names(ec2_client, args.targets)
#         print(f"Found instances: {instance_ids}")

#     valid_instance_ids = filter_valid_instances(instance_ids)
#     if not valid_instance_ids:
#         print("No valid instances found. Exiting.")
#         return

#     print(f"Targeting valid instances: {valid_instance_ids}")
#     command_id = run_shell_script(valid_instance_ids, script)
#     print(f"Command ID: {command_id}")

#     output = get_command_output(valid_instance_ids, command_id)
#     print("Command output:")

#     for instance_id, result in output.items():
#         print(f"Instance ID: {instance_id}")
#         print(f"Status: {result['Status']}")
#         print(f"Output: {result['Output']}")
#         print(f"Error: {result['Error']}")
#         print('-' * 60)