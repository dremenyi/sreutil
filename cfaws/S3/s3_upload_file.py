import boto3
import os
import logging
from botocore.exceptions import ClientError


def s3_upload_file(args):
    # Initialize session
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    s3 = session.client('s3')

    # Check if file exists
    if not os.path.isfile(args.path):
        print(f"File not found: {args.path}")
        return

    try:
        # Upload file
        s3.upload_file(args.path, args.bucket, args.key)
        print(f"Successfully uploaded {args.path} to {args.bucket}/{args.key}")

    except Exception as e:
        print(f"An error occurred while uploading the file: {str(e)}")
