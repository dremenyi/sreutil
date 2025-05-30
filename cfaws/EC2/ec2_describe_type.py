# # # # ec2_instance_type.py

# import boto3
# import textwrap
# from prettytable import PrettyTable as pretty

# def ec2_describe_type(args):
#     session = boto3.Session(profile_name=args.profile, region_name=args.region)
#     ec2 = session.resource('ec2')
#     ec2_client = session.client('ec2')

#     # Filtering instances by instance name or instance id
#     instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [args.name]}])

#     # Assuming only one instance matches the provided name
#     instance = list(instances)[0]
#     instance_type = instance.instance_type
    
#     response = ec2_client.describe_instance_types(
#         InstanceTypes=[
#             instance_type,
#         ],
#         Filters=[
#             {
#                 'Name': 'ebs-info.ebs-optimized-support',
#                 'Values': [
#                     'default',
#                 ]
#             },
#         ],
#     )

#     table = pretty(['Instance Type', 'Max Bandwidth(Mb/s)', 'Max IOPS', 'Max Throughput(MB/s)'])

#     for instance_type in response['InstanceTypes']:
#         ebs_info = instance_type['EbsInfo']['EbsOptimizedInfo']
#         table.add_row([
#             instance_type['InstanceType'], 
#             ebs_info['MaximumBandwidthInMbps'], 
#             ebs_info['MaximumIops'], 
#             ebs_info['MaximumThroughputInMBps']
#         ])

#     print(table)


# # # ec2_instance_type.py

# # import boto3
# # from prettytable import PrettyTable as pretty

# # def ec2_describe_type(args):
# #     profile = args.profile
# #     region = args.region
# #     instance_name = args.name
# #     session = boto3.Session(profile_name=profile, region_name=region)
# #     ec2 = session.resource('ec2')

# #     # Filtering instances by instance name or instance id
# #     instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])

# #     # Check if any instance was found
# #     if instances:
# #         instance = list(instances)[0]
# #         instance_type = instance.instance_type

# #         # Creating EC2 client to fetch instance type details
# #         ec2_client = session.client('ec2')
# #         instance_types = ec2_client.describe_instance_types(InstanceTypes=[instance_type])

# #         if instance_types and 'InstanceTypes' in instance_types and instance_types['InstanceTypes']:
# #             instance_type_details = instance_types['InstanceTypes'][0]

# #             table = pretty(['Instance Type', 'Max Bandwidth(Mb/s)', 'Max IOPS', 'Max Throughput(MB/s)', 
# #                             'Baseline IOPS', 'Max Network Throughput', 'Baseline Network Throughput', 
# #                             'Burstable Network Throughput'])

# #             table.add_row([
# #                 instance_type_details['InstanceType'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineBandwidthInMbps'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineIops'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineThroughputInMBps'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumBandwidthInMbps'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumIops'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumThroughputInMBps'],
# #                 instance_type_details['NetworkInfo']['MaximumNetworkInterfaces'],
# #                 instance_type_details['NetworkInfo']['Ipv6AddressesPerInterface'],
# #                 instance_type_details['NetworkInfo']['NetworkPerformance'],
# #                 instance_type_details['NetworkInfo']['EfaSupported'],
# #             ])
# #             print(table)
# #         else:
# #             print(f"No details found for instance type: {instance_type}")
# #     else:
# #         print(f"No instance found with name: {instance_name}")
 
 
 
#  # ec2_instance_type.py

# # import boto3
# # from prettytable import PrettyTable as pretty

# # def ec2_describe_type(args):
# #     profile = args.profile
# #     region = args.region
# #     instance_name = args.name
# #     session = boto3.Session(profile_name=profile, region_name=region)
# #     ec2 = session.resource('ec2')

# #     # Filtering instances by instance name or instance id
# #     instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [args.name]}])

# #     # Check if any instance was found
# #     if instances:
# #         instance = list(instances)[0]
# #         instance_type = instance.instance_type

# #         # Creating EC2 client to fetch instance type details
# #         ec2_client = session.client('ec2')
# #         instance_types = ec2_client.describe_instance_types(InstanceTypes=[instance_type])

# #         if instance_types and 'InstanceTypes' in instance_types and instance_types['InstanceTypes']:
# #             instance_type_details = instance_types['InstanceTypes'][0]

# #             table = pretty(['Instance Type', 'Max Bandwidth(Mb/s)', 'Max IOPS', 'Max Throughput(MB/s)', 
# #                             'Baseline IOPS', 'Max Network Throughput', 'Baseline Network Throughput'])

# #             table.add_row([
# #                 instance_type_details['InstanceType'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineBandwidthInMbps'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineIops'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineThroughputInMBps'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumBandwidthInMbps'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumIops'],
# #                 instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumThroughputInMBps'],
# #             ])
# #             print(table)
# #         else:
# #             print(f"No details found for instance type: {instance_type}")
# #     else:
# #         print(f"No instance found with name: {instance_name}")


# ec2_instance_type.py

import boto3
from prettytable import PrettyTable as pretty

def ec2_describe_type(args):
    profile = args.profile
    region = args.region
    instance_name = args.name
    session = boto3.Session(profile_name=profile, region_name=region)
    ec2 = session.resource('ec2')

    # Filtering instances by instance name or instance id
    instances = ec2.instances.filter(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])

    # Check if any instance was found
    if instances:
        instance = list(instances)[0]
        instance_type = instance.instance_type

        # Creating EC2 client to fetch instance type details
        ec2_client = session.client('ec2')
        instance_types = ec2_client.describe_instance_types(InstanceTypes=[instance_type])

        if instance_types and 'InstanceTypes' in instance_types and instance_types['InstanceTypes']:
            instance_type_details = instance_types['InstanceTypes'][0]

            table = pretty(['Instance Type', 'Max Bandwidth(Mb/s)', 'Max IOPS', 'Max Throughput(MB/s)', 
                            'Baseline Bandwidth(Mb/s)', 'Baseline IOPS', 'Baseline Throughput(MB/s)'])

            table.add_row([
                instance_type_details['InstanceType'],
                instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumBandwidthInMbps'],
                instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumIops'],
                instance_type_details['EbsInfo']['EbsOptimizedInfo']['MaximumThroughputInMBps'],
                instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineBandwidthInMbps'],
                instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineIops'],
                instance_type_details['EbsInfo']['EbsOptimizedInfo']['BaselineThroughputInMBps'],
            ])
            print(table)
        else:
            print(f"No details found for instance type: {instance_type}")
    else:
        print(f"No instance found with name: {instance_name}")

