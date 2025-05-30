# import boto3
# import csv
# from prettytable import PrettyTable

# def ec2_inventory(args, output_file=None):
    
#     session = boto3.Session(
#         profile_name=args.profile, 
#         region_name=args.region
                            
#                 )

#     ec2 = session.client('ec2')

#     result = []
#     response = ec2.describe_instances().get('Reservations')

#     # Create a PrettyTable instance
#     table = PrettyTable()
#     table.field_names = ['DNS Name', 'Name', 'Subnet', 'Instance Type', 'Private IP', 'Image ID']

#     for item in response:
#         for each in item['Instances']:
#             if "Tags" in each:
#                 name = None
#                 for tag in each['Tags']:
#                     if tag['Key'] == 'Name':
#                         name = tag['Value']

#                 # Check if the keys exist before accessing them
#                 dnsname = each['PrivateDnsName'] if 'PrivateDnsName' in each else 'N/A'
#                 subnet = each['SubnetId'] if 'SubnetId' in each else 'N/A'
#                 instance_type = each['InstanceType'] if 'InstanceType' in each else 'N/A'
#                 private_ip = each['PrivateIpAddress'] if 'PrivateIpAddress' in each else 'N/A'
#                 image_id = each['ImageId'] if 'ImageId' in each else 'N/A'

#                 # Append a row to the table
#                 table.add_row([dnsname, name, subnet, instance_type, private_ip, image_id])

#     # If output file is specified, write the table to the file in CSV format
#     if output_file:
#         with open(output_file, 'w') as file:
#             file.write(table.get_string())
#         print(f'Table written to file {output_file}.')
#     # Otherwise, print the table to the console
#     else:
#         print(table)


##VERSION 2 GRABS EVERYTHING XCEPT SUBNET NAME

# import boto3
# from prettytable import PrettyTable
# import argparse

# def ec2_inventory(args):
#     profile = args.profile
#     region = args.region
#     output = args.output

#     session = boto3.Session(profile_name=profile, region_name=region)
#     ec2 = session.resource('ec2')

#     table = PrettyTable()
#     table.field_names = ["Instance ID", "Instance Type", "Instance State", "Public IP", "Private IP", "Subnet ID", "Subnet Name", "VPC ID", "Name Tag"]

#     for instance in ec2.instances.all():
#         name_tag = ''
#         subnet_name = ''

#         if instance.tags:
#             for tag in instance.tags:
#                 if tag['Key'] == 'Name':
#                     name_tag = tag['Value']
#                 if tag['Key'] == 'Subnet':
#                     subnet_name = tag['Value']

#         subnet = instance.subnet
#         vpc = instance.vpc

#         table.add_row([instance.id, instance.instance_type, instance.state['Name'], instance.public_ip_address, instance.private_ip_address, subnet.id, subnet_name, vpc.id, name_tag])

#     if output:
#         with open(output, 'w') as f:
#             f.write(table.get_string())
#     else:
#         print(table)

# def main():
#     parser = argparse.ArgumentParser(description='Get EC2 inventory')
#     parser.add_argument('--profile', required=True, help='AWS profile to use')
#     parser.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
#     parser.add_argument('--output', help='Output CSV file')

#     args = parser.parse_args()
#     ec2_inventory(args)

# if __name__ == "__main__":
#     main()



import boto3
from prettytable import PrettyTable
import argparse

def ec2_inventory(args):
    profile = args.profile
    region = args.region
    output = args.output

    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')
    ec2_client = session.client('ec2')

    table = PrettyTable()
    table.field_names = ["Instance ID", "Instance Type", "Instance State", "Public IP", "Private IP", "Subnet ID", "Subnet Name", "VPC ID", "Name Tag"]

    for instance in ec2.instances.all():
        name_tag = ''
        subnet_name = ''

        if instance.tags:
            for tag in instance.tags:
                if tag['Key'] == 'Name':
                    name_tag = tag['Value']

        subnet = instance.subnet
        vpc = instance.vpc

        # Fetch the subnet details to get the subnet name
        if subnet:
            subnet_details = ec2_client.describe_subnets(SubnetIds=[subnet.id])
            for subnet_detail in subnet_details['Subnets']:
                for tag in subnet_detail.get('Tags', []):
                    if tag['Key'] == 'Name':
                        subnet_name = tag['Value']

        table.add_row([instance.id, instance.instance_type, instance.state['Name'], instance.public_ip_address, instance.private_ip_address, subnet.id if subnet else 'N/A', subnet_name, vpc.id if vpc else 'N/A', name_tag])

    if output:
        with open(output, 'w') as f:
            f.write(table.get_string())
    else:
        print(table)

def main():
    parser = argparse.ArgumentParser(description='Get EC2 inventory')
    parser.add_argument('--profile', required=True, help='AWS profile to use')
    parser.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser.add_argument('--output', help='Output CSV file')

    args = parser.parse_args()
    ec2_inventory(args)

if __name__ == "__main__":
    main()
