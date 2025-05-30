import argparse
import os
from EC2 import ec2_inventory, ec2_details, ec2_volume_details, ec2_describe_type, ec2_create_snapshot, ec2_replace_root_volume, ec2_list_snapshots, ec2_describe_snapshot, ec2_start_session, ec2_port_forward, ec2_run_shellscript, vpc_get_routes
#from RDS import rds_versions
from IAM import iam_audit, iam_user_report, iam_rotate_key, iam_set_role, iam_change_user_password
from SG import sg_inventory, sg_details
from INIT import init, re_init, man
from S3 import s3_download_file, s3_find_file, s3_upload_file, s3_delete_file, s3_bucket_list, list_s3_files, s3_get_properties
from SECRETSMANAGER import sm_list_secrets, sm_get_secret


def main():
    parser = argparse.ArgumentParser(description='AWS Get')
    subparsers = parser.add_subparsers(title='Commands', metavar='command', required=True)

     #####################
    #
    # INIT PARSERS
    #
    ######################
    
     # SHOW MANNUAL IN PRETTY TABLE FORMAT -- PRETTIER THAN USING THE CFAWS -H VIA ARGPARSE
    man_parser = subparsers.add_parser('man', help='Show manual in pretty table forman')
    #man_parser = subparsers.add_parser('man', help='Show manual')
    man_parser.set_defaults(func=man)

    # INIT PARSER
    init_parser = subparsers.add_parser('init', help='Initialize aws-fetch directories')
    init_parser.add_argument('--output', help='Specify the output directory for the aws-fetch folder (defaults to the Desktop)')
    init_parser.add_argument('--profile', help='Specify the AWS profile name to create a subdirectory under aws-fetch')
    init_parser.set_defaults(func=init)
    
    # REINIT PARSER
    re_init_parser = subparsers.add_parser('re-init', help='Re-initialize aws-fetch directories, removing any existing directories')
    re_init_parser.add_argument('--output', help='Specify the output directory for the aws-fetch folder (defaults to the Desktop)')
    re_init_parser.add_argument('--profile', help='Specify the AWS profile name to create a subdirectory under aws-fetch')
    re_init_parser.set_defaults(func=re_init)
    


    #####################
    #
    # EC2 PARSERS
    #
    ######################
    
    # EC2 INVENTORY PARSER
    ec2_inventory_parser = subparsers.add_parser('ec2-inventory', help='Get EC2 inventory')
    ec2_inventory_parser.add_argument('--profile', required=True, help='AWS profile to use')
    ec2_inventory_parser.add_argument('--region',default='us-gov-west-1', help='AWS region to use')
    ec2_inventory_parser.add_argument('--output', help='Output CSV file')
    ec2_inventory_parser.set_defaults(func=ec2_inventory)
    
    # EC2 DETAILS PARSER
    ec2_details_parser = subparsers.add_parser('ec2-details', help='Get EC2 instance details')
    ec2_details_parser.add_argument('--profile', required=True, help='AWS profile to use')
    ec2_details_parser.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    ec2_details_parser.add_argument('--name', required=True, help='EC2 instance name')
    ec2_details_parser.set_defaults(func=ec2_details)
    
    # EC2 START STOP PARSERS
    ec2_start_stop_parser = subparsers.add_parser('ec2-start-stop', description="Start or Stop an EC2 instance.")
    ec2_start_stop_parser.add_argument('--profile', type=str, required=True, help='AWS profile')
    ec2_start_stop_parser.add_argument('--region', type=str, required=True, help='AWS region')
    ec2_start_stop_parser.add_argument('--instance_id', type=str, required=True, help='Instance ID of the EC2 instance')
    ec2_start_stop_parser.add_argument('--action', type=str, required=True, help='Either "start" or "stop"')
    
    # EC2 VOLUME DETAILS PARSERS
    ec2_volume_details_parser = subparsers.add_parser('ec2-volume-details', description="Get all volumes attached to an EC2 instance.")
    ec2_volume_details_parser.add_argument('--profile', type=str, required=True, help='AWS profile')
    ec2_volume_details_parser.add_argument('--region', type=str, required=True, help='AWS region')
    ec2_volume_details_parser.add_argument('--instance', type=str, required=True, help='Instance ID of the EC2 instance')
    ec2_volume_details_parser.set_defaults(func=ec2_volume_details)
    
    # EC2 DESCRIBE TYPE PARSERS

    parser_ec2_instance_type = subparsers.add_parser('ec2-describe-type', help='Describe EC2 instance types.')
    parser_ec2_instance_type.add_argument('--profile', type=str, required=True, help='AWS profile')
    parser_ec2_instance_type.add_argument('--region', type=str, required=True, default='us-gov-west-1', help='AWS region')
    parser_ec2_instance_type.add_argument('--name', required=True, help='Name of the EC2 instance')
    parser_ec2_instance_type.set_defaults(func=ec2_describe_type)
    
    # EC2 SNAPSHOT PARSERS
    parser_ec2_snapshot = subparsers.add_parser('ec2-create-snapshot', help='Create a snapshot of the root volume of the specified EC2 instance')
    parser_ec2_snapshot.add_argument('--profile', type=str, required=True, help='AWS profile')
    parser_ec2_snapshot.add_argument('--region', type=str, default='us-gov-west-1', help='AWS region')
    parser_ec2_snapshot.add_argument('--name', help='The Name of the EC2 instance')
    parser_ec2_snapshot.add_argument('--show-progress', action='store_true', help='Show the snapshot creation progress')
    parser_ec2_snapshot.set_defaults(func=ec2_create_snapshot)
    
    # EC2 REPLACE ROOT VOLUME
    parser_replace_root_volume = subparsers.add_parser('ec2-replace-root-volume', help='Create a ReplaceRootVolumeTask for the specified EC2 instance')
    parser_replace_root_volume.add_argument('--profile', type=str, required=True, help='AWS profile')
    parser_replace_root_volume.add_argument('--region', type=str, default='us-gov-west-1', help='AWS region')
    parser_replace_root_volume.add_argument('--name', help='The Name of the EC2 instance')
    parser_replace_root_volume.add_argument('--snapshot-id', help='The ID of the snapshot')
    parser_replace_root_volume.add_argument('--ami-id', help='The ID of the AMI')
    parser_replace_root_volume.add_argument('--show-progress', action='store_true', help='Show the ReplaceRootVolumeTask progress')
    parser_replace_root_volume.set_defaults(func=ec2_replace_root_volume)
    
    # EC2 LIST SNAPSHOTS PARSER
    parser_list_snapshots = subparsers.add_parser('ec2-list-snapshots', description="List the last 15 snapshots taken of EC2 volumes.")
    parser_list_snapshots.add_argument('--profile', required=True, help='AWS profile to use')
    parser_list_snapshots.add_argument('--name', required=True, help='Name of EC2 snapshots')
    parser_list_snapshots.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_list_snapshots.set_defaults(func=ec2_list_snapshots)
    
    # EC2 DESCRIBE SNAPSHOT PARSER
    parser_describe_snapshot = subparsers.add_parser('ec2-describe-snapshot',description="Describe the status of a specified EC2 snapshot.")
    parser_describe_snapshot.add_argument('--profile', required=True, help='AWS profile to use')
    parser_describe_snapshot.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_describe_snapshot.add_argument('--snapshot-id', required=True, help='ID of the EC2 snapshot')
    parser_describe_snapshot.set_defaults(func=ec2_describe_snapshot)

    # EC2 START SESSION

    parser_start_session = subparsers.add_parser('ec2-start-session', description="Start a shell session with SSM (basically ssh)")
    parser_start_session.add_argument('--profile', required=True, help='AWS profile to use')
    parser_start_session.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_start_session.add_argument('--name', required=True, help='name of the EC2 instance')
    parser_start_session.set_defaults(func=ec2_start_session)

    # EC2 PORT FORWARD
    parser_port_forward = subparsers.add_parser('ec2-port-forward',description="Start a shell session with SSM (basically ssh)")
    parser_port_forward.add_argument('--profile', required=True, help='AWS profile to use')
    parser_port_forward.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_port_forward.add_argument('--name', required=True, help='name of the EC2 instance')
    parser_port_forward.add_argument('--port', required=True, help='Port the webapp is hosted on')
    parser_port_forward.add_argument('--local-port', required=True, help='Port you want to forward to')
    parser_port_forward.set_defaults(func=ec2_port_forward)

    # EC2 RUN SHELL SCRIPT
    parser_run_shellscript = subparsers.add_parser('ec2-run-shellscript', description="Run a shell script on EC2 instances using AWS Systems Manager")
    parser_run_shellscript.add_argument('--targets', nargs='*', help='List of instance names to target.')
    parser_run_shellscript.add_argument('--all-linux-instances', action='store_true', help='Target all running Linux instances.')
    parser_run_shellscript.add_argument('--file', type=str, required=True, help='Path to the shell script file to execute.')
    parser_run_shellscript.add_argument('--profile', required=True, help='AWS profile to use')
    parser_run_shellscript.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_run_shellscript.set_defaults(func=ec2_run_shellscript)

    # VPC / EC2 Get Routing
    parser_vpc_get_routes = subparsers.add_parser('vpc-get-routes', help='Get routes for VPCs and subnets')
    parser_vpc_get_routes.add_argument('--profile', required=True, help='AWS profile to use')
    parser_vpc_get_routes.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_vpc_get_routes.set_defaults(func=vpc_get_routes)


    
    #####################
    #
    # SG PARSERS
    #
    ######################
    
    # SG INVENTORY PARSER
    sg_inventory_parser = subparsers.add_parser('sg-inventory', help='Get security group inventory')
    sg_inventory_parser.add_argument('--profile', default='', help='AWS profile name')
    sg_inventory_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1)')
    sg_inventory_parser.add_argument('--output', default='security_groups.csv', help='Output file (default: security_groups.csv)')
    sg_inventory_parser.set_defaults(func=lambda args: sg_inventory(args.profile, args.region, args.output))
    
    # SG DETAILS PARSER
    sg_details_parser = subparsers.add_parser('sg-details', help='Get security group details')
    sg_details_parser.add_argument('--profile', required=True, help='AWS profile to use')
    sg_details_parser.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    sg_details_parser.add_argument('--name', required=True, help='Security group name')
    sg_details_parser.set_defaults(func=sg_details)
    
     #####################
    #
    # RDS PARSERS
    #
    ######################
    
    # GET RDS VERSIONS PARSER
    # rds_versions_parser = subparsers.add_parser('rds-versions', help='Get the latest versions of RDS systems')
    # rds_versions_parser.add_argument('--profile', default='', help='AWS profile name')
    # rds_versions_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1)')
    # rds_versions_parser.add_argument('--output', default='rds_versions.csv', help='Output file (default: rds_versions.csv)')
    # rds_versions_parser.set_defaults(func=lambda args: rds_versions(args.profile, args.region, args.output))
    
    #####################
    #
    # S3 PARSERS
    #
    ######################
    
    

    # LIST S3 BUCKETS
    parser_s3_bucket_list = subparsers.add_parser('s3-list-buckets', help='List all S3 buckets and their details.')
    parser_s3_bucket_list.add_argument('--profile', type=str, required=True, help='AWS profile')
    parser_s3_bucket_list.add_argument('--region', default='us-gov-west-1', type=str, required=True, help='AWS region')
    parser_s3_bucket_list.set_defaults(func=s3_bucket_list)

    
    # DOWNLOAD S3 FILE PARSER
    download_s3_file_parser = subparsers.add_parser('s3-download-file', help='Download file from S3 bucket')
    download_s3_file_parser.add_argument('--profile', default='', help='AWS profile name')
    download_s3_file_parser.add_argument('--bucket', default='qcs-fedramp-documentation', help='Name of the S3 bucket to download from')
    download_s3_file_parser.add_argument('--key', default='', help='S3 key to download (default: all files in the bucket)')
    download_s3_file_parser.add_argument('--output-dir', default=os.getcwd(), help='Directory to save downloaded files (default: current directory)')
    download_s3_file_parser.set_defaults(func=lambda args: s3_download_file(args.profile, args.bucket, args.key, args.output_dir))
    
    # LIST FILES IN AN S3 BUCKET
    parser_s3_list_files = subparsers.add_parser('s3-list-files', help='List files in an S3 bucket')
    parser_s3_list_files.add_argument('--profile', default='', help='AWS profile name')
    parser_s3_list_files.add_argument('--bucket', required=True, help='Name of the S3 bucket')
    parser_s3_list_files.set_defaults(func=list_s3_files)
    
    # FIND S3 FILE PARSER
    find_s3_file_parser = subparsers.add_parser('s3-find-file', help="Search for a file in S3.")
    find_s3_file_parser.add_argument('--profile', required=True, help='AWS profile to use')
    find_s3_file_parser.add_argument('--region', default='us-gov-west-1', help='AWS region (default: us-gov-west-1)')
    find_s3_file_parser.add_argument("--bucket", default = '', help="Specify the S3 bucket to search in.")
    find_s3_file_parser.add_argument("--key", help="Specify the S3 key prefix to search in.", default="")
    find_s3_file_parser.add_argument("--name", help="The file name to search for.")
    find_s3_file_parser.add_argument('--name-like', help='Pattern to match file names')

    find_s3_file_parser.set_defaults(func=s3_find_file)
    
    
    # UPLOAD S3 FILE PARSER
    parser_s3_upload_file = subparsers.add_parser('s3-upload-file', help='Upload a file to an S3 bucket.')
    parser_s3_upload_file.add_argument('--profile', required=True, help='AWS profile.')
    parser_s3_upload_file.add_argument('--region', default='us-gov-west-1', help='AWS region.')
    parser_s3_upload_file.add_argument('--bucket', required=True, help='S3 bucket name.')
    parser_s3_upload_file.add_argument('--path', required=True, help='Path of the file to upload.')
    parser_s3_upload_file.add_argument('--key', required=True, help='Key (name) for the file on S3.')
    parser_s3_upload_file.set_defaults(func=s3_upload_file)
    
    # DELETE S3 FILE PARSER
    parser_s3_upload_file = subparsers.add_parser('s3-delete-file', help='Delete a file to an S3 bucket.')
    parser_s3_upload_file.add_argument('--profile', required=True, help='AWS profile.')
    parser_s3_upload_file.add_argument('--region', default='us-gov-west-1', help='AWS region.')
    parser_s3_upload_file.add_argument('--bucket', required=True, help='S3 bucket name.')
    #parser_s3_upload_file.add_argument('--path', required=True, help='Path of the file to upload.')
    parser_s3_upload_file.add_argument('--key', required=True, help='Key (name) for the file on S3.')
    parser_s3_upload_file.set_defaults(func=s3_delete_file)

    parser_s3_get_properties = subparsers.add_parser('s3-get-properties', help='Get properties of S3 buckets')
    parser_s3_get_properties.add_argument('--profile', required=True, help='AWS profile to use')
    parser_s3_get_properties.add_argument('--region', default='us-gov-west-1', help='AWS region to use')
    parser_s3_get_properties.set_defaults(func=s3_get_properties)

    
    #####################
    #
    # IAM PARSERS
    #
    ######################
    
    # IAM AUDIT
    parser_iam_audit = subparsers.add_parser('iam-audit', help='Audits IAM users that have administrative access, mfa, and keys')
    parser_iam_audit.add_argument("--profile", required=True, help="AWS Profile to use.")
    parser_iam_audit.add_argument("--region", default='us-gov-west-1', help="AWS Region to use.")
    parser_iam_audit.set_defaults(func=iam_audit)
    
    # IAM USER REPORT
    parser_iam_user_report = subparsers.add_parser('iam-user-report', help='Audits IAM users that have administrative access, mfa, and keys')
    parser_iam_user_report.add_argument("--profile", required=True, help="AWS Profile to use.")
    parser_iam_user_report.add_argument("--region", default='us-gov-west-1', help="AWS Region to use.")
    parser_iam_user_report.set_defaults(func=iam_user_report)
    
    # IAM ROTATE KEY
    parser_iam_rotate_key = subparsers.add_parser('iam-rotate-key', help='Rotate IAM user access key')
    parser_iam_rotate_key.add_argument('--profile', required=True, help='AWS CLI Profile Name')
    parser_iam_rotate_key.add_argument('--region',default='us-gov-west-1', help='AWS Region')
    parser_iam_rotate_key.add_argument('--user', required=True, help='IAM User')
    parser_iam_rotate_key.set_defaults(func=iam_rotate_key)
    
    # IAM CHANGE USER PASSWORD
    parser_iam_change_user_password = subparsers.add_parser('iam-change-user-password', help='Rotate IAM user access key')
    parser_iam_change_user_password.add_argument('--profile', required=True, help='AWS CLI Profile Name')
    parser_iam_change_user_password.add_argument('--region',default='us-gov-west-1', help='AWS Region')
    parser_iam_change_user_password.add_argument('--user', required=True, help='IAM User')
    parser_iam_change_user_password.set_defaults(func=iam_rotate_key)

    # IAM ASSUME ROLE 
    parser_iam_assume_role = subparsers.add_parser('iam-assume-role', help='Assume CMS CLI ADMIN Role')
    parser_iam_assume_role.add_argument('--profile', required=True, help='AWS CLI Profile Name')
    parser_iam_assume_role.add_argument('--region',default='us-gov-west-1', help='AWS Region')
    parser_iam_assume_role.add_argument('--token', required=True, help='Your MFA Token')
    parser_iam_assume_role.set_defaults(func=iam_set_role)
    
    
    #####################
    #
    # SECRETS MANAGER PARSERS
    #
    ######################
    
     # SECRETS MANAGER - LIST SECRETS PARSER
    parser_list_secrets = subparsers.add_parser('sm-list-secrets', help='Rotate IAM user access key')
    parser_list_secrets.add_argument('--profile', required=True, help='AWS CLI Profile Name')
    parser_list_secrets.add_argument('--region',default='us-gov-west-1', help='AWS Region')
    parser_list_secrets.set_defaults(func=sm_list_secrets)
    
    parser_get_secret = subparsers.add_parser('sm-get-secret', help='Rotate IAM user access key')
    parser_get_secret.add_argument('--profile', required=True, help='AWS CLI Profile Name')
    parser_get_secret.add_argument('--region',default='us-gov-west-1', help='AWS Region')
    parser_get_secret.add_argument('--name-like',required=True, help='AWS Region')
    parser_get_secret.set_defaults(func=sm_get_secret)
    
    # Standard args output #
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
