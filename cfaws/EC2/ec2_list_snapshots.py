import boto3
import argparse
from prettytable import PrettyTable

def ec2_list_snapshots(args):
    session = boto3.Session(
        profile_name=args.profile,
        region_name=args.region
    )
    ec2 = session.client('ec2')
    snapshot_response = ec2.describe_snapshots(
        OwnerIds=['self'], 
        Filters=[
            {
                'Name': 'status',
                'Values': [
                    'pending',
                    'completed',
                ]
            },
        ],
    )

    # Filter snapshots by name tag
    filtered_snapshots = [snapshot for snapshot in snapshot_response['Snapshots'] if 'Tags' in snapshot and any(tag['Key'] == 'Name' and tag['Value'] == args.name for tag in snapshot['Tags'])]

    # Sort snapshots by date of creation
    filtered_snapshots.sort(key=lambda x: x['StartTime'], reverse=True)

    # Create prettytable and set its field names
    x = PrettyTable()
    x.field_names = ['Name', 'Snapshot', 'Creation Date', 'Status']

    # Add snapshots' information to the table
    for snapshot in filtered_snapshots[:15]:
        name = next((tag['Value'] for tag in snapshot.get('Tags', []) if tag['Key'] == 'Name'), '')
        snapshot_id = snapshot.get('SnapshotId', '')
        creation_date = snapshot.get('StartTime', '')
        status = snapshot.get('State', '')
        x.add_row([name, snapshot_id, creation_date, status])

    # Print the table
    print(x)