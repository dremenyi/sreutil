import boto3
import argparse
from botocore.config import Config
from colorama import Fore, Style, init
import time
import fnmatch

def s3_find_file(args):
    
    profile = args.profile
    region = args.region
    key = args.key
    file = args.name
    name_like = args.name_like
    bucket_name = args.bucket
    
    # Initialize colorama
    init(autoreset=True)

    session = boto3.Session(region_name=region, profile_name=profile)
    
    config = Config(signature_version='s3v4')
    s3 = session.client("s3", config=config)
    
    paginator = s3.get_paginator("list_objects_v2")

    if not bucket_name:
        buckets = s3.list_buckets()["Buckets"]
    else:
        buckets = [{"Name": bucket_name}]
        
    start_time = time.time()

    file_links = []
    for bucket in buckets:
        bucket_name = bucket["Name"]
        for page in paginator.paginate(Bucket=bucket_name, Prefix=key):
            for obj in page.get("Contents", []):
                # If a pattern is provided, only process files that match the pattern
                if name_like:
                    if not fnmatch.fnmatch(obj["Key"], f"*{name_like}*"):
                        continue
                elif not obj["Key"].endswith(file):
                    continue
                
                url = s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket_name, "Key": obj["Key"]},
                    ExpiresIn=3600,
                )
                file_links.append((obj["Key"], url))

    end_time = time.time()  # Record the end time
    time_taken = end_time - start_time

    print(f"{Fore.GREEN}Found the following files: {len(file_links)}\n")
    print("Download links:")
    for file_name, url in file_links:
        print(f"\n{Fore.GREEN}{file_name}{Style.RESET_ALL}\n\n{Fore.YELLOW}{url}{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}Time taken to find the files: {time_taken:.2f} seconds{Style.RESET_ALL}")
    print(f"{Fore.RED}Finished searching.{Style.RESET_ALL}")
