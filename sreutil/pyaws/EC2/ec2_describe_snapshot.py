import boto3
from prettytable import PrettyTable

def ec2_describe_snapshot(args):
    session = boto3.Session(
        profile_name=args.profile,
        region_name=args.region
    )
    ec2 = session.client('ec2')

    snapshot_response = ec2.describe_snapshots(
        SnapshotIds=[args.snapshot_id],
    )

    if len(snapshot_response['Snapshots']) == 0:
        print(Fore.RED + "No snapshot found with the given ID: " + args.snapshot_id + Style.RESET_ALL)
        return

    snapshot = snapshot_response['Snapshots'][0]

    # Create prettytable and set its field names
    x = PrettyTable()
    x.field_names = ['Snapshot ID', 'Volume ID', 'State', 'Start Time', 'Progress', 'Volume Size']

    # Add snapshot's information to the table
    snapshot_id = snapshot.get('SnapshotId', '')
    volume_id = snapshot.get('VolumeId', '')
    state = snapshot.get('State', '')
    start_time = snapshot.get('StartTime', '')
    progress = snapshot.get('Progress', '')
    volume_size = snapshot.get('VolumeSize', '')
    
    x.add_row([snapshot_id, volume_id, state, start_time, progress, volume_size])

    # Print the table
    print(x)