import boto3
from botocore.exceptions import ClientError
import argparse
from prettytable import PrettyTable

def get_s3_bucket_encryption(s3_client, bucket_name):
    try:
        result = s3_client.get_bucket_encryption(Bucket=bucket_name)
        rules = result['ServerSideEncryptionConfiguration']['Rules']
        key_arn = rules[0]['ApplyServerSideEncryptionByDefault'].get('KMSMasterKeyID', 'Default')
        key_name = key_arn.split('/')[-1] if 'arn:aws:kms' in key_arn else 'AWS S3 Managed Key'
        return "ENCRYPTED", key_arn, key_name
    except ClientError as e:
        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
            return "NOT ENCRYPTED", None, None
        else:
            raise e

def s3_get_properties(args):
    profile = args.profile
    region = args.region

    session = boto3.Session(profile_name=profile, region_name=region)
    s3_client = session.client('s3')

    buckets = s3_client.list_buckets()
    table = PrettyTable()
    table.field_names = ["Bucket Name", "Encryption Status", "Key ARN", "Key Name"]

    for bucket in buckets['Buckets']:
        bucket_name = bucket['Name']
        encryption_status, key_arn, key_name = get_s3_bucket_encryption(s3_client, bucket_name)
        table.add_row([bucket_name, encryption_status, key_arn if key_arn else "N/A", key_name if key_name else "N/A"])

    print(table)