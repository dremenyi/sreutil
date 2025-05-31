# import os
# import shutil
# import textwrap
# import prettytable

# # def init(args):
# #     base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
# #     base_path = os.path.join(base_path, "aws-fetch")
# #     services = ["IAM", "RDS", "EC2", "SG"]

# #     if args.profile:
# #         base_path = os.path.join(base_path, args.profile)

# #     if not os.path.exists(base_path):
# #         os.makedirs(base_path)

# #     for service in services:
# #         service_path = os.path.join(base_path, service)
# #         if not os.path.exists(service_path):
# #             os.makedirs(service_path)

# #     print(f"Initialized aws-fetch directories at {base_path}.")
    
# def init(args):
#     base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
#     base_path = os.path.join(base_path, "aws-fetch")

#     if args.profile:
#         base_path = os.path.join(base_path, args.profile)
#         if not os.path.exists(base_path):
#             os.makedirs(base_path)

#     module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     services = [d for d in os.listdir(module_path) if os.path.isdir(os.path.join(module_path, d)) and d != "INIT" and d != "__pycache__" and d!= 'aws_fetch.egg-info']

#     for service in services:
#         service_path = os.path.join(base_path, service)
#         if not os.path.exists(service_path):
#             os.makedirs(service_path)

#     print(f"Initialized aws-fetch directories at {base_path}.")


# def re_init(args):
#     base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
#     base_path = os.path.join(base_path, "aws-fetch")

#     if args.profile:
#         base_path = os.path.join(base_path, args.profile)

#     if os.path.exists(base_path):
#         shutil.rmtree(base_path)

#     os.makedirs(base_path)

#     module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     services = [d for d in os.listdir(module_path) if os.path.isdir(os.path.join(module_path, d)) and d != "INIT" and d != "__pycache__" and d!= 'aws_fetch.egg-info']

#     for service in services:
#         service_path = os.path.join(base_path, service)
#         if not os.path.exists(service_path):
#             os.makedirs(service_path)

#     print(f"Re-initialized aws-fetch directories at {base_path}.")
    


# def man(args):
#     ec2_table = prettytable.PrettyTable()
#     ec2_table.title = 'EC2 Commands'
#     ec2_table.field_names = ["Command", "Description", "Arguments"]
#     ec2_table.add_row(["ec2-inventory", "\n".join(textwrap.wrap("Get EC2 inventory", 150)), "\n".join(textwrap.wrap("--profile, --region, --output", 150))])
#     ec2_table.add_row(["ec2-details", "\n".join(textwrap.wrap("Get EC2 instance details", 150)), "\n".join(textwrap.wrap("--profile, --name", 150))])
#     ec2_table.add_row(["ec2-describe-type", "\n".join(textwrap.wrap("Describe EC2 instance types", 150)), "\n".join(textwrap.wrap("--profile, --region, --name", 150))])
#     ec2_table.add_row(["ec2-create-snapshot", "\n".join(textwrap.wrap("Create a snapshot of the root volume of the specified EC2 instance", 150)), "\n".join(textwrap.wrap("--profile, --region, --name (Name of server to snapshot root volume of), --show-progress", 150))])
#     ec2_table.add_row(["ec2-replace-root-volume", "\n".join(textwrap.wrap("Create a ReplaceRootVolumeTask for the specified EC2 instance", 150)), "\n".join(textwrap.wrap("--profile --region --name --snapshot-id --ami-id --show-progress", 150))])
#     ec2_table.add_row(["ec2-list-snapshots", "\n".join(textwrap.wrap("List the last 15 snapshots of EC2 volumes", 150)), "\n".join(textwrap.wrap("arguments are required: --profile, --name", 150))])
#     ec2_table.add_row(["ec2-describe-snapshot", "\n".join(textwrap.wrap("Describe the status of a snapshot", 150)), "\n".join(textwrap.wrap("the following arguments are required: --profile, --snapshot-id", 150))])
#     ec2_table.add_row(["ec2-start-session", "\n".join(textwrap.wrap("Starts an SSM session in your local shell", 150)), "\n".join(textwrap.wrap("the following arguments are required: --profile, --name <name of instance you want to shell to>", 150))])
#     ec2_table.add_row(["ec2-port-forward", "\n".join(textwrap.wrap("Forwards EC2 port to localhost", 150)), "\n".join(textwrap.wrap("the following arguments are required: --profile, --name <name of instance to initiate port forward>, --port <port of the webapp> --local-port <local port you want to foward to>", 150))])


#     s3_table = prettytable.PrettyTable()
#     s3_table.title = 'S3 Commands'
#     s3_table.field_names = ["Command", "Description"]
#     s3_table.add_row(["s3-list-buckets", "List all S3 buckets and their details"])
#     s3_table.add_row(["s3-download-file", "Download file from S3 bucket"])
#     s3_table.add_row(["s3-list-files", "List files in an S3 bucket"])
#     s3_table.add_row(["s3-find-file", "Search for a file in S3"])
#     s3_table.add_row(["s3-upload-file", "Upload a file to an S3 bucket"])
#     s3_table.add_row(["s3-delete-file", "Delete a file from an S3 bucket"])

#     sm_table = prettytable.PrettyTable()
#     sm_table.title = 'Secrets Manager Commands'
#     sm_table.field_names = ["Command", "Description"]
#     sm_table.add_row(["sm-list-secrets", "List secrets in Secrets Manager"])
#     sm_table.add_row(["sm-get-secret", "Retrieve a specific secret from Secrets Manager"])

#     sg_table = prettytable.PrettyTable()
#     sg_table.title = 'Security Group Commands'
#     sg_table.field_names = ["Command", "Description"]
#     sg_table.add_row(["sg-inventory", "Get security group inventory"])
#     sg_table.add_row(["sg-details", "Get security group details"])

#     rds_table = prettytable.PrettyTable()
#     rds_table.title = 'RDS Commands'
#     rds_table.field_names = ["Command", "Description"]
#     rds_table.add_row(["rds-versions", "Get the latest versions of RDS systems"])

#     iam_table = prettytable.PrettyTable()
#     iam_table.title = 'IAM Commands'
#     iam_table.field_names = ["Command", "Description"]
#     # IAM FUTURE TABLE
#     iam_table.add_row(["iam-list-users", "List IAM users"])
#     iam_table.add_row(["iam-user-details", "Get IAM user details"])

#     # Add the tables to the print statement in the man function
#     print(ec2_table, "\n")
#     print(s3_table, "\n")
#     print(sm_table, "\n")
#     print(sg_table, "\n")
#     print(rds_table, "\n")
#     print(iam_table, "\n")



import os
import shutil
import textwrap
import prettytable

# This function initializes directories for aws-fetch output.
# It determines the base path, optionally creates a profile-specific subdirectory,
# and then creates subdirectories for various AWS services.
def init_pyaws_dirs(args):
    """
    Initializes directories for pyaws 'aws-fetch' output.
    Creates a base 'aws-fetch' directory, an optional profile-specific subdirectory,
    and subdirectories for various AWS services.
    """
    base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
    base_path = os.path.join(base_path, "aws-fetch") # Root folder for fetched AWS data

    if args.profile: # If a profile is specified, create a subdirectory for it
        base_path = os.path.join(base_path, args.profile)
    
    if not os.path.exists(base_path): # Create the base path if it doesn't exist
        os.makedirs(base_path)
        print(f"Created base directory: {base_path}")
    else:
        print(f"Base directory already exists: {base_path}")

    # Define expected service directories for pyaws
    services = ["IAM", "RDS", "EC2", "SG", "S3", "SECRETSMANAGER"] # Add other relevant services

    for service in services:
        service_path = os.path.join(base_path, service)
        if not os.path.exists(service_path):
            os.makedirs(service_path)
            print(f"Created service directory: {service_path}")
        else:
            print(f"Service directory already exists: {service_path}")

    print(f"Finished initializing pyaws 'aws-fetch' directories at {base_path}.")


# This function re-initializes aws-fetch directories.
# It removes existing directories if they exist and then creates them anew.
def re_init_pyaws_dirs(args):
    """
    Re-initializes pyaws 'aws-fetch' directories.
    Removes the existing 'aws-fetch' (and profile-specific) directory if it exists,
    then creates it anew along with service subdirectories.
    """
    base_path = os.path.expanduser(args.output) if args.output else os.path.join(os.path.expanduser("~"), "Desktop")
    base_path = os.path.join(base_path, "aws-fetch")

    if args.profile:
        base_path = os.path.join(base_path, args.profile)

    if os.path.exists(base_path): # If the base path exists, remove it
        print(f"Removing existing directory: {base_path}")
        shutil.rmtree(base_path)

    print(f"Creating base directory: {base_path}")
    os.makedirs(base_path) # Create the base path

    # Define expected service directories
    services = ["IAM", "RDS", "EC2", "SG", "S3", "SECRETSMANAGER"] # Add other relevant services

    for service in services:
        service_path = os.path.join(base_path, service)
        os.makedirs(service_path) # Create service directory
        print(f"Created service directory: {service_path}")

    print(f"Finished re-initializing pyaws 'aws-fetch' directories at {base_path}.")


# This function displays the manual for pyaws commands in a pretty table format.
def pyaws_man_page(args):
    """
    Displays the command manual for the 'pyaws' tool, outlining various AWS service commands,
    their descriptions, and typical arguments using prettytable.
    """
    print("\n--- PYAWS Command Manual ---")

    # EC2 Commands Table
    ec2_table = prettytable.PrettyTable()
    ec2_table.title = 'PYAWS - EC2 Commands'
    ec2_table.field_names = ["Command", "Description", "Common Arguments"]
    ec2_table.align["Command"] = "l"
    ec2_table.align["Description"] = "l"
    ec2_table.align["Common Arguments"] = "l"
    ec2_table.add_row(["ec2-inventory", textwrap.fill("Get EC2 inventory.", 60), "--profile, --region, --output"])
    ec2_table.add_row(["ec2-details", textwrap.fill("Get details for a specific EC2 instance.", 60), "--profile, --region, --name"])
    ec2_table.add_row(["ec2-describe-type", textwrap.fill("Describe EC2 instance types (EBS optimized info).", 60), "--profile, --region, --name"])
    ec2_table.add_row(["ec2-create-snapshot", textwrap.fill("Create snapshot of an EC2 instance's root volume.", 60), "--profile, --region, --name, --show-progress"])
    ec2_table.add_row(["ec2-replace-root-volume", textwrap.fill("Replace root volume of an EC2 instance from snapshot or AMI.", 60), "--profile, --region, --name, --snapshot-id OR --ami-id, --show-progress"])
    ec2_table.add_row(["ec2-list-snapshots", textwrap.fill("List recent snapshots for an EC2 instance (by name tag).", 60), "--profile, --region, --name"])
    ec2_table.add_row(["ec2-describe-snapshot", textwrap.fill("Describe a specific snapshot's status.", 60), "--profile, --region, --snapshot-id"])
    ec2_table.add_row(["ec2-start-session", textwrap.fill("Start an SSM session to an EC2 instance.", 60), "--profile, --region, --name"])
    ec2_table.add_row(["ec2-port-forward", textwrap.fill("Forward a local port to an EC2 instance port via SSM.", 60), "--profile, --region, --name, --port, --local-port"])
    ec2_table.add_row(["ec2-run-shellscript", textwrap.fill("Run a shell script on EC2 instances via SSM.", 60), "--profile, --region, --targets OR --all-linux-instances, --file"])
    ec2_table.add_row(["ec2-volume-details", textwrap.fill("Get details of volumes attached to an EC2 instance.", 60), "--profile, --region, --instance"])
    ec2_table.add_row(["ec2-start-stop", textwrap.fill("Start or stop an EC2 instance.", 60), "--profile, --region, --instance_id, --action (start|stop)"])
    ec2_table.add_row(["vpc-get-routes", textwrap.fill("Get route table information for VPCs and subnets.", 60), "--profile, --region"])
    print(ec2_table)

    # S3 Commands Table
    s3_table = prettytable.PrettyTable()
    s3_table.title = 'PYAWS - S3 Commands'
    s3_table.field_names = ["Command", "Description", "Common Arguments"]
    s3_table.align["Command"] = "l"
    s3_table.align["Description"] = "l"
    s3_table.align["Common Arguments"] = "l"
    s3_table.add_row(["s3-list-buckets", textwrap.fill("List all S3 buckets.", 60), "--profile, --region"])
    s3_table.add_row(["s3-list-files", textwrap.fill("List files in an S3 bucket.", 60), "--profile, --region, --bucket"])
    s3_table.add_row(["s3-download-file", textwrap.fill("Download file(s) from an S3 bucket.", 60), "--profile, --region, --bucket, --key, --output-dir"])
    s3_table.add_row(["s3-find-file", textwrap.fill("Search for a file in S3 and get a presigned URL.", 60), "--profile, --region, --bucket (opt), --key (prefix), --name OR --name-like"])
    s3_table.add_row(["s3-upload-file", textwrap.fill("Upload a file to an S3 bucket.", 60), "--profile, --region, --bucket, --path, --key"])
    s3_table.add_row(["s3-delete-file", textwrap.fill("Delete a file from an S3 bucket.", 60), "--profile, --region, --bucket, --key"])
    s3_table.add_row(["s3-get-properties", textwrap.fill("Get encryption properties of S3 buckets.", 60), "--profile, --region"])
    print(s3_table)

    # Secrets Manager Commands Table
    sm_table = prettytable.PrettyTable()
    sm_table.title = 'PYAWS - Secrets Manager Commands'
    sm_table.field_names = ["Command", "Description", "Common Arguments"]
    sm_table.align["Command"] = "l"
    sm_table.align["Description"] = "l"
    sm_table.align["Common Arguments"] = "l"
    sm_table.add_row(["sm-list-secrets", textwrap.fill("List secrets (filtered by common paths).", 60), "--profile, --region"])
    sm_table.add_row(["sm-get-secret", textwrap.fill("Retrieve secrets matching a name pattern.", 60), "--profile, --region, --name-like"])
    print(sm_table)

    # Security Group Commands Table
    sg_table = prettytable.PrettyTable()
    sg_table.title = 'PYAWS - Security Group Commands'
    sg_table.field_names = ["Command", "Description", "Common Arguments"]
    sg_table.align["Command"] = "l"
    sg_table.align["Description"] = "l"
    sg_table.align["Common Arguments"] = "l"
    sg_table.add_row(["sg-inventory", textwrap.fill("Get security group inventory.", 60), "--profile, --region, --output (csv)"])
    sg_table.add_row(["sg-details", textwrap.fill("Get details for a specific security group.", 60), "--profile, --region, --name"])
    print(sg_table)

    # RDS Commands Table
    rds_table = prettytable.PrettyTable()
    rds_table.title = 'PYAWS - RDS Commands'
    rds_table.field_names = ["Command", "Description", "Common Arguments"]
    rds_table.align["Command"] = "l"
    rds_table.align["Description"] = "l"
    rds_table.align["Common Arguments"] = "l"
    rds_table.add_row(["rds-versions", textwrap.fill("Check RDS instance versions against newer available ones.", 60), "--profile, --region, --output (csv)"])
    print(rds_table)

    # IAM Commands Table
    iam_table = prettytable.PrettyTable()
    iam_table.title = 'PYAWS - IAM Commands'
    iam_table.field_names = ["Command", "Description", "Common Arguments"]
    iam_table.align["Command"] = "l"
    iam_table.align["Description"] = "l"
    iam_table.align["Common Arguments"] = "l"
    iam_table.add_row(["iam-audit", textwrap.fill("Audit IAM users (MFA, policies, key age/use).", 60), "--profile, --region"])
    iam_table.add_row(["iam-user-report", textwrap.fill("Generate IAM user credential report.", 60), "--profile, --region, --csv_path (opt)"])
    iam_table.add_row(["iam-rotate-key", textwrap.fill("Manage IAM user access keys (create/deactivate).", 60), "--profile, --region, --user"])
    iam_table.add_row(["iam-change-user-password", textwrap.fill("Change/create an IAM user's console password.", 60), "--profile, --region, --user"])
    iam_table.add_row(["iam-assume-role", textwrap.fill("Assume 'CLI_ADMIN' role with MFA.", 60), "--profile, --region, --token"])
    print(iam_table)
    print("\nUse 'sreutil pyaws <command> -h' for specific options on each command.")



