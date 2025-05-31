import boto3

def s3_delete_file(args):
    # Initialize session
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    s3 = session.client('s3')

    try:
        # Delete file
        s3.delete_object(Bucket=args.bucket, Key=args.key)
        print(f"Successfully deleted {args.key} from {args.bucket}")

    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")