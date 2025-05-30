import os
import shutil
import textwrap

# def init(args):
#     base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
#     base_path = os.path.join(base_path, "aws-fetch")
#     services = ["IAM", "RDS", "EC2", "SG"]

#     if args.profile:
#         base_path = os.path.join(base_path, args.profile)

#     if not os.path.exists(base_path):
#         os.makedirs(base_path)

#     for service in services:
#         service_path = os.path.join(base_path, service)
#         if not os.path.exists(service_path):
#             os.makedirs(service_path)

#     print(f"Initialized aws-fetch directories at {base_path}.")
    
def init(args):
    base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
    base_path = os.path.join(base_path, "aws-fetch")

    if args.profile:
        base_path = os.path.join(base_path, args.profile)
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    services = [d for d in os.listdir(module_path) if os.path.isdir(os.path.join(module_path, d)) and d != "INIT" and d != "__pycache__" and d!= 'aws_fetch.egg-info']

    for service in services:
        service_path = os.path.join(base_path, service)
        if not os.path.exists(service_path):
            os.makedirs(service_path)

    print(f"Initialized aws-fetch directories at {base_path}.")


def re_init(args):
    base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
    base_path = os.path.join(base_path, "aws-fetch")

    if args.profile:
        base_path = os.path.join(base_path, args.profile)

    if os.path.exists(base_path):
        shutil.rmtree(base_path)

    os.makedirs(base_path)

    module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    services = [d for d in os.listdir(module_path) if os.path.isdir(os.path.join(module_path, d)) and d != "INIT" and d != "__pycache__" and d!= 'aws_fetch.egg-info']

    for service in services:
        service_path = os.path.join(base_path, service)
        if not os.path.exists(service_path):
            os.makedirs(service_path)

    print(f"Re-initialized aws-fetch directories at {base_path}.")
    

import prettytable


def man(args):
    ec2_table = prettytable.PrettyTable()
    ec2_table.title = 'EC2 Commands'
    ec2_table.field_names = ["Command", "Description", "Arguments"]
    ec2_table.add_row(["ec2-inventory", "\n".join(textwrap.wrap("Get EC2 inventory", 150)), "\n".join(textwrap.wrap("--profile, --region, --output", 150))])
    ec2_table.add_row(["ec2-details", "\n".join(textwrap.wrap("Get EC2 instance details", 150)), "\n".join(textwrap.wrap("--profile, --name", 150))])
    ec2_table.add_row(["ec2-describe-type", "\n".join(textwrap.wrap("Describe EC2 instance types", 150)), "\n".join(textwrap.wrap("--profile, --region, --name", 150))])
    ec2_table.add_row(["ec2-create-snapshot", "\n".join(textwrap.wrap("Create a snapshot of the root volume of the specified EC2 instance", 150)), "\n".join(textwrap.wrap("--profile, --region, --name (Name of server to snapshot root volume of), --show-progress", 150))])
    ec2_table.add_row(["ec2-replace-root-volume", "\n".join(textwrap.wrap("Create a ReplaceRootVolumeTask for the specified EC2 instance", 150)), "\n".join(textwrap.wrap("--profile --region --name --snapshot-id --ami-id --show-progress", 150))])
    ec2_table.add_row(["ec2-list-snapshots", "\n".join(textwrap.wrap("List the last 15 snapshots of EC2 volumes", 150)), "\n".join(textwrap.wrap("arguments are required: --profile, --name", 150))])
    ec2_table.add_row(["ec2-describe-snapshot", "\n".join(textwrap.wrap("Describe the status of a snapshot", 150)), "\n".join(textwrap.wrap("the following arguments are required: --profile, --snapshot-id", 150))])
    ec2_table.add_row(["ec2-start-session", "\n".join(textwrap.wrap("Starts an SSM session in your local shell", 150)), "\n".join(textwrap.wrap("the following arguments are required: --profile, --name <name of instance you want to shell to>", 150))])
    ec2_table.add_row(["ec2-port-forward", "\n".join(textwrap.wrap("Forwards EC2 port to localhost", 150)), "\n".join(textwrap.wrap("the following arguments are required: --profile, --name <name of instance to initiate port forward>, --port <port of the webapp> --local-port <local port you want to foward to>", 150))])


    s3_table = prettytable.PrettyTable()
    s3_table.title = 'S3 Commands'
    s3_table.field_names = ["Command", "Description"]
    s3_table.add_row(["s3-list-buckets", "List all S3 buckets and their details"])
    s3_table.add_row(["s3-download-file", "Download file from S3 bucket"])
    s3_table.add_row(["s3-list-files", "List files in an S3 bucket"])
    s3_table.add_row(["s3-find-file", "Search for a file in S3"])
    s3_table.add_row(["s3-upload-file", "Upload a file to an S3 bucket"])
    s3_table.add_row(["s3-delete-file", "Delete a file from an S3 bucket"])

    sm_table = prettytable.PrettyTable()
    sm_table.title = 'Secrets Manager Commands'
    sm_table.field_names = ["Command", "Description"]
    sm_table.add_row(["sm-list-secrets", "List secrets in Secrets Manager"])
    sm_table.add_row(["sm-get-secret", "Retrieve a specific secret from Secrets Manager"])

    sg_table = prettytable.PrettyTable()
    sg_table.title = 'Security Group Commands'
    sg_table.field_names = ["Command", "Description"]
    sg_table.add_row(["sg-inventory", "Get security group inventory"])
    sg_table.add_row(["sg-details", "Get security group details"])

    rds_table = prettytable.PrettyTable()
    rds_table.title = 'RDS Commands'
    rds_table.field_names = ["Command", "Description"]
    rds_table.add_row(["rds-versions", "Get the latest versions of RDS systems"])

    iam_table = prettytable.PrettyTable()
    iam_table.title = 'IAM Commands'
    iam_table.field_names = ["Command", "Description"]
    # IAM FUTURE TABLE
    iam_table.add_row(["iam-list-users", "List IAM users"])
    iam_table.add_row(["iam-user-details", "Get IAM user details"])

    # Add the tables to the print statement in the man function
    print(ec2_table, "\n")
    print(s3_table, "\n")
    print(sm_table, "\n")
    print(sg_table, "\n")
    print(rds_table, "\n")
    print(iam_table, "\n")


 



