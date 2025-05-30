# s3_bucket_list.py

import boto3
import textwrap
from prettytable import PrettyTable as pretty

def s3_bucket_list(args):
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    s3_resource = session.resource('s3')
    s3_client = session.client('s3')

    table = pretty(['Bucket Name', 'Creation Date', 'Bucket Location'])

    for bucket in s3_resource.buckets.all():
        try:
            location = s3_client.get_bucket_location(Bucket=bucket.name)['LocationConstraint']
        except Exception as e:
            location = 'Error'

        # Wrap content of the cells
        wrapped_name = "\n".join(textwrap.wrap(bucket.name, 30))
        wrapped_location = "\n".join(textwrap.wrap(location if location else 'us-east-1', 30))

        table.add_row([wrapped_name, bucket.creation_date, wrapped_location])

    print(table)
