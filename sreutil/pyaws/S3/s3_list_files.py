import boto3
import prettytable
from botocore.exceptions import NoCredentialsError

def list_s3_files(args):
    session = boto3.Session(profile_name=args.profile)
    s3 = session.resource('s3')
    bucket = s3.Bucket(args.bucket)

    table = prettytable.PrettyTable()
    table.field_names = ["Files Found In " f"{args.bucket}"]
    table.align["File Name"] = "l"
    table.max_width = 60

    try:
        for obj in bucket.objects.all():
            table.add_row([obj.key])
    except NoCredentialsError:
        print("No AWS credentials found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print(table)
