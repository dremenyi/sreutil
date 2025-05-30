import boto3
import argparse
from prettytable import PrettyTable

def vpc_get_routes(args):
    profile = args.profile
    region = args.region

    session = boto3.Session(profile_name=profile, region_name=region)
    ec2_client = session.client('ec2')

    # Get all VPCs
    vpcs = ec2_client.describe_vpcs()
    table = PrettyTable()
    table.field_names = ["VPC ID", "Subnet ID", "Route Table ID", "Destination", "Target", "Description"]

    for vpc in vpcs['Vpcs']:
        vpc_id = vpc['VpcId']
        
        # Get all subnets in the VPC
        subnets = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
        for subnet in subnets['Subnets']:
            subnet_id = subnet['SubnetId']
            
            # Get the route tables for each subnet
            route_tables = ec2_client.describe_route_tables(Filters=[{'Name': 'association.subnet-id', 'Values': [subnet_id]}])
            for route_table in route_tables['RouteTables']:
                route_table_id = route_table['RouteTableId']
                for route in route_table['Routes']:
                    destination = route.get('DestinationCidrBlock', 'N/A')
                    target = route.get('GatewayId') or route.get('NatGatewayId') or route.get('NetworkInterfaceId') or 'N/A'
                    description = route.get('Description', 'N/A')
                    table.add_row([vpc_id, subnet_id, route_table_id, destination, target, description])

    print(table)
