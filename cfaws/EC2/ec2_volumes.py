import boto3
import textwrap
from prettytable import PrettyTable as pretty

def ec2_volume_details(args):
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    ec2_resource = session.resource('ec2')

    filters = [{'Name': 'instance-id', 'Values': [args.instance]}] if args.instance.startswith('i-') else [{'Name': 'tag:Name', 'Values': [args.instance]}]

    instances = ec2_resource.instances.filter(Filters=filters)

    table = pretty(['Instance Name','Instance ID', 'Volume ID', 'State', 'Size (GB)', 'Type', 'IOPS', 'Delete on Termination'])

    for instance in instances:
        instance_name = next((tag['Value'] for tag in instance.tags if tag['Key'] == 'Name'), None)
        block_device_mappings = instance.block_device_mappings
        for block_device in block_device_mappings:
            volume_id = block_device['Ebs']['VolumeId']
            volume = ec2_resource.Volume(volume_id)

            # Wrap content of the cells
            wrapped_instance_name = "\n".join(textwrap.wrap(instance_name, 30))
            wrapped_instance_id = "\n".join(textwrap.wrap(instance.id, 30))
            wrapped_volume_id = "\n".join(textwrap.wrap(volume.id, 30))
            wrapped_state = "\n".join(textwrap.wrap(volume.state, 30))
            wrapped_type = "\n".join(textwrap.wrap(volume.volume_type, 30))

            table.add_row([wrapped_instance_name, wrapped_instance_id, wrapped_volume_id, wrapped_state, volume.size, wrapped_type, volume.iops, block_device['Ebs']['DeleteOnTermination']])

    print(table)
