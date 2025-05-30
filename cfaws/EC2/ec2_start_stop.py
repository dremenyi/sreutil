import boto3
import argparse

def start_stop_ec2(args):
    session = boto3.Session(profile_name=args.profile, region_name=args.region)
    ec2_resource = session.resource('ec2')

    instance = ec2_resource.Instance(args.instance_id)

    if args.action == "start":
        instance.start()
        print(f"Starting instance: {args.instance_id}")
    elif args.action == "stop":
        instance.stop()
        print(f"Stopping instance: {args.instance_id}")