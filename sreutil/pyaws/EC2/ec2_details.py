import boto3
import textwrap
from prettytable import PrettyTable as pretty
# Reserve for future TODO:
import os
import csv

def ec2_details(args):
    table = pretty(['EC2 Instance Name', 'InstanceID', 'EC2 Instance Status', 'Status Checks', 'Private DNS Name', 'Private IP Address', 'Attached Security Groups', 'Associated Tags'])

    profile = args.profile
    region = args.region
    ec2_name = args.name
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')
    ec2_client = session.client('ec2')
    
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [ec2_name]}])
    

    for instance in instances:
        name_tag = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), None)
        instance_id = instance.id

        security_group_names = [sg['GroupName'] for sg in instance.security_groups]
        security_groups = ', '.join(security_group_names)

        instance_status_response = ec2_client.describe_instance_status(InstanceIds=[instance.id])
        if instance_status_response['InstanceStatuses']:
            instance_status = instance_status_response['InstanceStatuses'][0]['InstanceStatus']['Status']
            system_status = instance_status_response['InstanceStatuses'][0]['SystemStatus']['Status']
            status_checks = f"{instance_status} / {system_status}"
        else:
            status_checks = "Not available"

        associated_tags = ', '.join(['{}={}'.format(tag['Key'], tag['Value']) for tag in instance.tags])

        # Wrap content of the cells
        wrapped_name_tag = "\n".join(textwrap.wrap(name_tag, 30))
        wrapped_security_groups = "\n".join(textwrap.wrap(security_groups, 30))
        wrapped_tags = "\n".join(textwrap.wrap(associated_tags, 30))
        
        table.add_row([wrapped_name_tag, instance.state['Name'], instance_id, status_checks, instance.private_dns_name, instance.private_ip_address, wrapped_security_groups, wrapped_tags])

    print(table)
    
    csv_output = table.get_csv_string()
    with open("output.csv", "w") as f:
     f.write(csv_output)

