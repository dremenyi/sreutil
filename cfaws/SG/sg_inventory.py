import boto3
import csv
import os

def sg_inventory(profile_name, region_name, output_file):
    session = boto3.Session(
        region_name=region_name,
        profile_name=profile_name
    )

    # Set up EC2 client
    ec2 = session.client('ec2')

    # Retrieve all security groups
    sgs = ec2.describe_security_groups()

    # Open CSV file for writing
    with open('security_groups.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(['Security Group Name', 'Description', 'Inbound Rules', 'Outbound Rules'])

        # Write data rows for each security group
        for sg in sgs['SecurityGroups']:
            # Get security group name and description
            name = sg['GroupName']
            description = sg['Description']

            # Get inbound rules
            inbound_rules = []
            for rule in sg['IpPermissions']:
                protocol = rule['IpProtocol']
                if protocol == '-1':
                    protocol = 'All'
                from_port = rule.get('FromPort', 'All')
                to_port = rule.get('ToPort', 'All')
                cidrs = []
                for ip_range in rule['IpRanges']:
                    cidrs.append(ip_range['CidrIp'])
                for group in rule['UserIdGroupPairs']:
                    cidrs.append(group['GroupId'])
                inbound_rules.append(f'{protocol} ({from_port}-{to_port}): {", ".join(cidrs)}')

            # Get outbound rules
            outbound_rules = []
            for rule in sg['IpPermissionsEgress']:
                protocol = rule['IpProtocol']
                if protocol == '-1':
                    protocol = 'All'
                from_port = rule.get('FromPort', 'All')
                to_port = rule.get('ToPort', 'All')
                cidrs = []
                for ip_range in rule['IpRanges']:
                    cidrs.append(ip_range['CidrIp'])
                for group in rule['UserIdGroupPairs']:
                    cidrs.append(group['GroupId'])
                outbound_rules.append(f'{protocol} ({from_port}-{to_port}): {", ".join(cidrs)}')

            # Write data row
            writer.writerow([name, description, "\n".join(inbound_rules), "\n".join(outbound_rules)])

    print('Security groups exported to security_groups.csv')