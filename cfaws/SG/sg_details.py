import boto3
import os
import csv
from prettytable import PrettyTable as pretty

def sg_details(args):
    profile = args.profile
    region = args.region
    sg_name = args.name

    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')

    security_group = None
    for sg in ec2.security_groups.all():
        if sg.group_name == sg_name:
            security_group = sg
            break

    if not security_group:
        print(f"Security group '{sg_name}' not found.")
        return
    print()
    print(f"Security Group Name: {sg_name}")
    print(f"Description: {security_group.description}\n")

    print("Inbound Rules:")
    table = pretty(['Protocol', 'Port Range', 'Source', 'Description'])
    for rule in security_group.ip_permissions:
        protocol = rule['IpProtocol']
        from_port = rule.get('FromPort', 'All')
        to_port = rule.get('ToPort', 'All')
        for ip_range in rule['IpRanges']:
            source = ip_range['CidrIp']
            description = ip_range.get('Description', 'no description')
            table.add_row([protocol, f"{from_port}-{to_port}", source, description])
    print(table)

    print("\nOutbound Rules:")
    table = pretty(['Protocol', 'Port Range', 'Destination', 'Description'])
    for rule in security_group.ip_permissions_egress:
        protocol = rule['IpProtocol']
        from_port = rule.get('FromPort', 'All')
        to_port = rule.get('ToPort', 'All')
        for ip_range in rule['IpRanges']:
            destination = ip_range['CidrIp']
            description = ip_range.get('Description', 'no description')
            table.add_row([protocol, f"{from_port}-{to_port}", destination, description])
    print(table)