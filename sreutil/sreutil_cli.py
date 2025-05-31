# Latest
# sreutil/sreutil_cli.py
import argparse
import os

# --- Import SREUTIL common functions ---
# Assuming you will create this or have created it for a top-level sreutil manual
# from .common.manual import sreutil_top_level_man_func # Placeholder

# --- Import PYAWS helper functions ---
from .pyaws.helpers.init_aws import init_pyaws_dirs, re_init_pyaws_dirs, pyaws_man_page

# --- Import PYAWS command functions ---
# EC2
from .pyaws.EC2.ec2_inventory import ec2_inventory
from .pyaws.EC2.ec2_details import ec2_details
from .pyaws.EC2.ec2_start_stop import start_stop_ec2
from .pyaws.EC2.ec2_volumes import ec2_volume_details
from .pyaws.EC2.ec2_describe_type import ec2_describe_type
from .pyaws.EC2.ec2_root_vol_snapshot import ec2_create_snapshot
from .pyaws.EC2.ec2_replace_root_volume import ec2_replace_root_volume
from .pyaws.EC2.ec2_list_snapshots import ec2_list_snapshots
from .pyaws.EC2.ec2_describe_snapshot import ec2_describe_snapshot
from .pyaws.EC2.ec2_start_session import ec2_start_session
from .pyaws.EC2.ec2_port_forward import ec2_port_forward
from .pyaws.EC2.ec2_run_shellscript import ec2_run_shellscript
from .pyaws.EC2.vpc_get_routes import vpc_get_routes


# IAM
from .pyaws.IAM import iam_audit                 # Corrected
from .pyaws.IAM import iam_user_report           # Corrected
from .pyaws.IAM import iam_rotate_key            # Corrected
from .pyaws.IAM import iam_change_user_password  # Corrected
from .pyaws.IAM import iam_set_role              # Corrected

# SG
from .pyaws.SG.sg_inventory import sg_inventory
from .pyaws.SG.sg_details import sg_details

# S3
from .pyaws.S3.s3_list_buckets import s3_bucket_list
from .pyaws.S3.s3_download_file import s3_download_file
from .pyaws.S3.s3_list_files import list_s3_files # Note: original function name
from .pyaws.S3.s3_find_file import s3_find_file
from .pyaws.S3.s3_upload_file import s3_upload_file
from .pyaws.S3.s3_delete_file import s3_delete_file
from .pyaws.S3.s3_get_properties import s3_get_properties

# SECRETSMANAGER
from .pyaws.SECRETSMANAGER.sm_list_secrets import sm_list_secrets
from .pyaws.SECRETSMANAGER.sm_get_secret import sm_get_secret

# RDS
# Assuming rds_versions is in sreutil/pyaws/RDS/rds_versions.py
# and sreutil/pyaws/RDS/__init__.py exists
from .pyaws.RDS.rds_versions import rds_versions


# Placeholder for sreutil_top_level_man_func if you create it
def sreutil_top_level_man_func(args):
    print("SREUTIL - Top Level Manual (Placeholder)")
    print("Available tools:")
    print("  pyaws         - Collection of AWS utilities")
    print("\nUse 'sreutil <tool> man' or 'sreutil <tool> --help' for tool-specific help.")
    print("Use 'sreutil pyaws <command> -h' for command-specific help.")


def main():
    # Top-level parser for 'sreutil'
    parser = argparse.ArgumentParser(
        description='SRE Utility Toolkit. Provides various tools for SRE tasks.',
        formatter_class=argparse.RawTextHelpFormatter # Allows for better help text formatting
    )
    parser.add_argument('--version', action='version', version='%(prog)s 0.1.0') # Example version
    sreutil_subparsers = parser.add_subparsers(
        title='Available Tools',
        description="Run 'sreutil <tool> -h' for more information on a specific tool.",
        dest='tool_name',
        metavar="<tool>"
    )
    sreutil_subparsers.required = False # Allow 'sreutil' and 'sreutil man'

    # --- SREUTIL top-level 'man' command ---
    man_parser_sreutil = sreutil_subparsers.add_parser(
        'man',
        help='Show the top-level manual for SREUTIL.',
        description='Displays an overview of the SREUTIL toolkit and its available tools.'
    )
    man_parser_sreutil.set_defaults(func=sreutil_top_level_man_func)

    # --- PYAWS Tool ---
    pyaws_parser = sreutil_subparsers.add_parser(
        'pyaws',
        help='Suite of AWS (Amazon Web Services) command-line utilities.',
        description='Provides commands for interacting with various AWS services like EC2, S3, IAM, etc.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    pyaws_subparsers = pyaws_parser.add_subparsers(
        title='PYAWS Commands',
        description="Run 'sreutil pyaws <command> -h' for more information on a specific command.",
        dest='pyaws_command_name',
        metavar="<command>"
    )
    pyaws_subparsers.required = False # Allow 'sreutil pyaws' and 'sreutil pyaws man'

    # --- PYAWS Helper Commands (man, init-dirs, reinit-dirs) ---
    pyaws_man_parser = pyaws_subparsers.add_parser(
        'man',
        help='Show the manual for PYAWS commands.',
        description='Displays a detailed list of all available PYAWS commands and their general arguments.'
    )
    pyaws_man_parser.set_defaults(func=pyaws_man_page)

    pyaws_init_parser = pyaws_subparsers.add_parser(
        'init-dirs',
        help='Initialize "aws-fetch" directories for PYAWS outputs.',
        description="Creates a standard directory structure (Desktop/aws-fetch/<profile>/<service>) for storing output files from PYAWS commands."
    )
    pyaws_init_parser.add_argument('--output', help='Specify the base output directory (defaults to ~/Desktop).')
    pyaws_init_parser.add_argument('--profile', help='AWS profile name to create a subdirectory under "aws-fetch".')
    pyaws_init_parser.set_defaults(func=init_pyaws_dirs)

    pyaws_reinit_parser = pyaws_subparsers.add_parser(
        'reinit-dirs',
        help='Re-initialize "aws-fetch" directories (removes existing ones).',
        description="Warning: This will delete the existing 'aws-fetch' directory (and its profile-specific subdirectories if specified) before recreating it."
    )
    pyaws_reinit_parser.add_argument('--output', help='Specify the base output directory (defaults to ~/Desktop).')
    pyaws_reinit_parser.add_argument('--profile', help='AWS profile name for the subdirectory.')
    pyaws_reinit_parser.set_defaults(func=re_init_pyaws_dirs)

    # --- PYAWS EC2 Commands ---
    ec2_inventory_parser = pyaws_subparsers.add_parser('ec2-inventory', help='Get EC2 inventory.')
    ec2_inventory_parser.add_argument('--profile', required=True, help='AWS profile to use.')
    ec2_inventory_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    ec2_inventory_parser.add_argument('--output', help='Optional: Path to output CSV file.')
    ec2_inventory_parser.set_defaults(func=ec2_inventory)

    ec2_details_parser = pyaws_subparsers.add_parser('ec2-details', help='Get detailed information for a specific EC2 instance.')
    ec2_details_parser.add_argument('--profile', required=True, help='AWS profile to use.')
    ec2_details_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    ec2_details_parser.add_argument('--name', required=True, help='Name tag of the EC2 instance.')
    ec2_details_parser.set_defaults(func=ec2_details)

    ec2_start_stop_parser = pyaws_subparsers.add_parser('ec2-start-stop', help="Start or Stop an EC2 instance.")
    ec2_start_stop_parser.add_argument('--profile', type=str, required=True, help='AWS profile.')
    ec2_start_stop_parser.add_argument('--region', type=str, required=True, help='AWS region.')
    ec2_start_stop_parser.add_argument('--instance-id', type=str, required=True, help='Instance ID of the EC2 instance.')
    ec2_start_stop_parser.add_argument('--action', type=str, required=True, choices=['start', 'stop'], help='Action to perform: "start" or "stop".')
    ec2_start_stop_parser.set_defaults(func=start_stop_ec2)

    ec2_volume_details_parser = pyaws_subparsers.add_parser('ec2-volume-details', help="Get details of volumes attached to an EC2 instance.")
    ec2_volume_details_parser.add_argument('--profile', type=str, required=True, help='AWS profile.')
    ec2_volume_details_parser.add_argument('--region', type=str, required=True, help='AWS region.')
    ec2_volume_details_parser.add_argument('--instance', type=str, required=True, help='Instance ID or Name tag of the EC2 instance.')
    ec2_volume_details_parser.set_defaults(func=ec2_volume_details)

    parser_ec2_instance_type = pyaws_subparsers.add_parser('ec2-describe-type', help='Describe EBS-optimized info for an EC2 instance type.')
    parser_ec2_instance_type.add_argument('--profile', type=str, required=True, help='AWS profile.')
    parser_ec2_instance_type.add_argument('--region', type=str, default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_ec2_instance_type.add_argument('--name', required=True, help='Name tag of the EC2 instance to find its type.')
    parser_ec2_instance_type.set_defaults(func=ec2_describe_type)

    parser_ec2_snapshot = pyaws_subparsers.add_parser('ec2-create-snapshot', help="Create a snapshot of an EC2 instance's root volume.")
    parser_ec2_snapshot.add_argument('--profile', type=str, required=True, help='AWS profile.')
    parser_ec2_snapshot.add_argument('--region', type=str, default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_ec2_snapshot.add_argument('--name', required=True, help='Name tag of the EC2 instance.')
    parser_ec2_snapshot.add_argument('--show-progress', action='store_true', help='Display snapshot creation progress (experimental).')
    parser_ec2_snapshot.set_defaults(func=ec2_create_snapshot)

    parser_replace_root_volume = pyaws_subparsers.add_parser('ec2-replace-root-volume', help='Replace the root volume of an EC2 instance.')
    parser_replace_root_volume.add_argument('--profile', type=str, required=True, help='AWS profile.')
    parser_replace_root_volume.add_argument('--region', type=str, default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_replace_root_volume.add_argument('--name', required=True, help='Name tag of the EC2 instance.')
    group_snap_ami = parser_replace_root_volume.add_mutually_exclusive_group(required=True)
    group_snap_ami.add_argument('--snapshot-id', help='ID of the snapshot to use for replacement.')
    group_snap_ami.add_argument('--ami-id', help='ID of the AMI to use for replacement.')
    parser_replace_root_volume.add_argument('--show-progress', action='store_true', help='Display task progress (experimental).')
    parser_replace_root_volume.set_defaults(func=ec2_replace_root_volume)

    parser_list_snapshots = pyaws_subparsers.add_parser('ec2-list-snapshots', help="List recent snapshots for an EC2 instance (by name tag).")
    parser_list_snapshots.add_argument('--profile', required=True, help='AWS profile.')
    parser_list_snapshots.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_list_snapshots.add_argument('--name', required=True, help='Name tag of the EC2 instance for which to list snapshots.')
    parser_list_snapshots.set_defaults(func=ec2_list_snapshots)

    parser_describe_snapshot = pyaws_subparsers.add_parser('ec2-describe-snapshot', help="Describe a specific EC2 snapshot.")
    parser_describe_snapshot.add_argument('--profile', required=True, help='AWS profile.')
    parser_describe_snapshot.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_describe_snapshot.add_argument('--snapshot-id', required=True, help='ID of the EC2 snapshot.')
    parser_describe_snapshot.set_defaults(func=ec2_describe_snapshot)

    parser_start_session = pyaws_subparsers.add_parser('ec2-start-session', help="Start an SSM session to an EC2 instance.")
    parser_start_session.add_argument('--profile', required=True, help='AWS profile.')
    parser_start_session.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_start_session.add_argument('--name', required=True, help='Name tag of the target EC2 instance.')
    parser_start_session.set_defaults(func=ec2_start_session)

    parser_port_forward = pyaws_subparsers.add_parser('ec2-port-forward', help="Forward a local port to an EC2 instance port via SSM.")
    parser_port_forward.add_argument('--profile', required=True, help='AWS profile.')
    parser_port_forward.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_port_forward.add_argument('--name', required=True, help='Name tag of the target EC2 instance.')
    parser_port_forward.add_argument('--port', required=True, help='Remote port on the EC2 instance.')
    parser_port_forward.add_argument('--local-port', required=True, help='Local port to forward from.')
    parser_port_forward.set_defaults(func=ec2_port_forward)

    parser_run_shellscript = pyaws_subparsers.add_parser('ec2-run-shellscript', help="Run a shell script on EC2 instances via SSM.")
    parser_run_shellscript.add_argument('--profile', required=True, help='AWS profile.')
    parser_run_shellscript.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_run_shellscript.add_argument('--file', type=str, required=True, help='Path to the shell script file to execute.')
    group_targets = parser_run_shellscript.add_mutually_exclusive_group(required=True)
    group_targets.add_argument('--targets', nargs='*', help='List of instance Name tags to target.')
    group_targets.add_argument('--all-linux-instances', action='store_true', help='Target all running Linux instances managed by SSM.')
    parser_run_shellscript.set_defaults(func=ec2_run_shellscript)
    
    parser_vpc_get_routes = pyaws_subparsers.add_parser('vpc-get-routes', help='Get route table information for VPCs and subnets.')
    parser_vpc_get_routes.add_argument('--profile', required=True, help='AWS profile to use.')
    parser_vpc_get_routes.add_argument('--region', default='us-gov-west-1', help='AWS region to use (default: us-gov-west-1).')
    parser_vpc_get_routes.set_defaults(func=vpc_get_routes)

    # --- PYAWS SG Commands ---
    sg_inventory_parser = pyaws_subparsers.add_parser('sg-inventory', help='Get security group inventory.')
    sg_inventory_parser.add_argument('--profile', required=True, help='AWS profile name.') # Made required for consistency
    sg_inventory_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    sg_inventory_parser.add_argument('--output', default='security_groups.csv', help='Output CSV file (default: security_groups.csv).')
    sg_inventory_parser.set_defaults(func=lambda args_sg_inv: sg_inventory(args_sg_inv.profile, args_sg_inv.region, args_sg_inv.output)) # Original lambda was fine

    sg_details_parser = pyaws_subparsers.add_parser('sg-details', help='Get details for a specific security group.')
    sg_details_parser.add_argument('--profile', required=True, help='AWS profile.')
    sg_details_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    sg_details_parser.add_argument('--name', required=True, help='Name of the security group.')
    sg_details_parser.set_defaults(func=sg_details)

    # --- PYAWS RDS Commands ---
    rds_versions_parser = pyaws_subparsers.add_parser('rds-versions', help='Check RDS instance versions against newer available ones.')
    rds_versions_parser.add_argument('--profile', required=True, help='AWS profile name.') # Made required
    rds_versions_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    rds_versions_parser.add_argument('--output', default='rds_versions.csv', help='Output CSV file (default: rds_versions.csv).')
    rds_versions_parser.set_defaults(func=lambda args_rds_ver: rds_versions(args_rds_ver.profile, args_rds_ver.region, args_rds_ver.output)) # Original lambda

    # --- PYAWS S3 Commands ---
    parser_s3_bucket_list = pyaws_subparsers.add_parser('s3-list-buckets', help='List all S3 buckets.')
    parser_s3_bucket_list.add_argument('--profile', type=str, required=True, help='AWS profile.')
    parser_s3_bucket_list.add_argument('--region', type=str, default='us-gov-west-1', help='AWS region (default: us-gov-west-1).') # Original had required=True
    parser_s3_bucket_list.set_defaults(func=s3_bucket_list)

    download_s3_file_parser = pyaws_subparsers.add_parser('s3-download-file', help='Download file(s) from an S3 bucket.')
    download_s3_file_parser.add_argument('--profile', required=True, help='AWS profile name.') # Made required
    download_s3_file_parser.add_argument('--region', default='us-gov-west-1', help='AWS region for session (default: us-gov-west-1).') # Added region
    download_s3_file_parser.add_argument('--bucket', required=True, help='Name of the S3 bucket.') # Made required
    download_s3_file_parser.add_argument('--key', default='', help='S3 key prefix or full key of the file(s) to download (default: all files).')
    download_s3_file_parser.add_argument('--output-dir', default=os.getcwd(), help='Directory to save downloaded files (default: current directory).')
    download_s3_file_parser.set_defaults(func=lambda args_s3_dl: s3_download_file(args_s3_dl.profile, args_s3_dl.bucket, args_s3_dl.key, args_s3_dl.output_dir))


    parser_s3_list_files = pyaws_subparsers.add_parser('s3-list-files', help='List files in an S3 bucket.')
    parser_s3_list_files.add_argument('--profile', required=True, help='AWS profile name.') # Made required
    parser_s3_list_files.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).') # Added region argument
    parser_s3_list_files.add_argument('--bucket', required=True, help='Name of the S3 bucket.')
    parser_s3_list_files.set_defaults(func=list_s3_files) # list_s3_files needs to be able to handle args.region if it uses it

    find_s3_file_parser = pyaws_subparsers.add_parser('s3-find-file', help="Search for a file in S3 and get a presigned URL.")
    find_s3_file_parser.add_argument('--profile', required=True, help='AWS profile.')
    find_s3_file_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    find_s3_file_parser.add_argument("--bucket", help="Optional: Specify a single S3 bucket to search in.")
    find_s3_file_parser.add_argument("--key", default="", help="Optional: S3 key prefix to narrow down the search.")
    group_name_like = find_s3_file_parser.add_mutually_exclusive_group(required=True)
    group_name_like.add_argument("--name", help="Exact file name to search for.")
    group_name_like.add_argument('--name-like', help='Pattern to match in file names (e.g., "*.zip").')
    find_s3_file_parser.set_defaults(func=s3_find_file)

    parser_s3_upload_file = pyaws_subparsers.add_parser('s3-upload-file', help='Upload a file to an S3 bucket.')
    parser_s3_upload_file.add_argument('--profile', required=True, help='AWS profile.')
    parser_s3_upload_file.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_s3_upload_file.add_argument('--bucket', required=True, help='Target S3 bucket name.')
    parser_s3_upload_file.add_argument('--path', required=True, help='Local path of the file to upload.')
    parser_s3_upload_file.add_argument('--key', required=True, help='Target key (name) for the file on S3.')
    parser_s3_upload_file.set_defaults(func=s3_upload_file)

    parser_s3_delete_file = pyaws_subparsers.add_parser('s3-delete-file', help='Delete a file from an S3 bucket.') # Corrected variable name
    parser_s3_delete_file.add_argument('--profile', required=True, help='AWS profile.')
    parser_s3_delete_file.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_s3_delete_file.add_argument('--bucket', required=True, help='S3 bucket name.')
    parser_s3_delete_file.add_argument('--key', required=True, help='Key (name) of the file to delete on S3.')
    parser_s3_delete_file.set_defaults(func=s3_delete_file)

    parser_s3_get_properties = pyaws_subparsers.add_parser('s3-get-properties', help='Get encryption properties of S3 buckets.')
    parser_s3_get_properties.add_argument('--profile', required=True, help='AWS profile.')
    parser_s3_get_properties.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_s3_get_properties.set_defaults(func=s3_get_properties)

    # --- PYAWS IAM Commands ---
    parser_iam_audit = pyaws_subparsers.add_parser('iam-audit', help='Audit IAM users (MFA, policies, access key age/use).')
    parser_iam_audit.add_argument("--profile", required=True, help="AWS Profile.")
    parser_iam_audit.add_argument("--region", default='us-gov-west-1', help="AWS Region (default: us-gov-west-1).")
    parser_iam_audit.set_defaults(func=iam_audit)

    parser_iam_user_report = pyaws_subparsers.add_parser('iam-user-report', help='Generate IAM user credential report.')
    parser_iam_user_report.add_argument("--profile", required=True, help="AWS Profile.")
    parser_iam_user_report.add_argument("--region", default='us-gov-west-1', help="AWS Region (default: us-gov-west-1).")
    parser_iam_user_report.add_argument("--csv-path", help="Optional: Path to save the report as a CSV file.")
    parser_iam_user_report.set_defaults(func=iam_user_report)

    parser_iam_rotate_key = pyaws_subparsers.add_parser('iam-rotate-key', help='Manage IAM user access keys (create/deactivate).')
    parser_iam_rotate_key.add_argument('--profile', required=True, help='AWS profile.')
    parser_iam_rotate_key.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_iam_rotate_key.add_argument('--user', required=True, help='IAM User name.')
    parser_iam_rotate_key.set_defaults(func=iam_rotate_key)

    parser_iam_change_user_password = pyaws_subparsers.add_parser('iam-change-user-password', help="Change or create an IAM user's console password.")
    parser_iam_change_user_password.add_argument('--profile', required=True, help='AWS profile.')
    parser_iam_change_user_password.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_iam_change_user_password.add_argument('--user', required=True, help='IAM User name.')
    parser_iam_change_user_password.set_defaults(func=iam_change_user_password) # Corrected from iam_rotate_key

    parser_iam_assume_role = pyaws_subparsers.add_parser('iam-assume-role', help="Assume the 'CLI_ADMIN' role with MFA.")
    parser_iam_assume_role.add_argument('--profile', required=True, help='AWS profile to use for initial STS call.')
    parser_iam_assume_role.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_iam_assume_role.add_argument('--token', required=True, help='Your MFA token code.')
    parser_iam_assume_role.set_defaults(func=iam_set_role)

# --- PYAWS SECRETSMANAGER Commands ---
    parser_sm_list_secrets = pyaws_subparsers.add_parser('sm-list-secrets', help='List secrets in Secrets Manager, with filtering.')
    parser_sm_list_secrets.add_argument('--profile', required=True, help='AWS profile.')
    parser_sm_list_secrets.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_sm_list_secrets.add_argument('--include-keywords', nargs='*', help='Space-separated keywords. Secret names containing ANY of these will be included (case-insensitive).')
    parser_sm_list_secrets.add_argument('--exclude-keywords', nargs='*', help='Space-separated keywords. Secret names containing ANY of these will be excluded (case-insensitive).')
    parser_sm_list_secrets.add_argument('--fetch-values', action='store_true', help='Actually fetch the content of the secrets. If not set, only metadata is shown.')
    parser_sm_list_secrets.add_argument('--show-values', action='store_true', help='Display the actual secret values. Requires --fetch-values. USE WITH EXTREME CAUTION.')
    parser_sm_list_secrets.set_defaults(func=sm_list_secrets)


    parser_sm_get_secret = pyaws_subparsers.add_parser('sm-get-secret', help='Retrieve secrets from Secrets Manager matching a name pattern.')
    parser_sm_get_secret.add_argument('--profile', required=True, help='AWS profile.')
    parser_sm_get_secret.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1).')
    parser_sm_get_secret.add_argument('--name-like', required=True, help='Pattern to match in secret names.')
    parser_sm_get_secret.set_defaults(func=sm_get_secret)

    # --- Argument parsing and execution ---
    args = parser.parse_args()

    if args.tool_name is None and not hasattr(args, 'func'): # 'sreutil' called alone
        parser.print_help()
    elif args.tool_name == 'pyaws' and args.pyaws_command_name is None and not hasattr(args, 'func'): # 'sreutil pyaws' called alone
        pyaws_parser.print_help()
    elif hasattr(args, 'func'):
        args.func(args)
    else:
        # This case should ideally not be reached if subparsers are configured correctly
        # or if 'required=True' is used on subparser destinations where appropriate.
        # However, if a tool is called without a command and that tool itself doesn't have a default action.
        if args.tool_name == 'pyaws':
             pyaws_parser.print_help()
        else:
             parser.print_help()


if __name__ == '__main__':
    main()