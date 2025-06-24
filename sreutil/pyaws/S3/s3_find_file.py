import boto3
import botocore # For ClientError
from botocore.config import Config
from colorama import Fore, Style, init
import time
import fnmatch
import os # For os.path.basename

def s3_find_file(args):
    profile = args.profile
    region = args.region
    key_prefix_filter = args.key if args.key is not None else "" # Ensure it's a string for Prefix
    exact_file_name = args.name
    name_like_pattern = args.name_like
    target_bucket_name = args.bucket

    init(autoreset=True)

    print(f"{Fore.CYAN}Initializing S3 client for region '{region}' with profile '{profile}'...{Style.RESET_ALL}")
    session = boto3.Session(region_name=region, profile_name=profile)
    s3_client_config = Config(signature_version='s3v4', retries={'max_attempts': 5, 'mode': 'standard'})
    s3 = session.client("s3", config=s3_client_config)
    
    paginator = s3.get_paginator("list_objects_v2")

    buckets_to_search = []
    if target_bucket_name:
        #Add a quick check if the specified bucket is accessible by trying to get its location.
        try:
            s3.head_bucket(Bucket=target_bucket_name) # Checks existence and permissions
            buckets_to_search.append({"Name": target_bucket_name})
            print(f"{Fore.CYAN}Targeting specified bucket: {target_bucket_name}{Style.RESET_ALL}")
        except botocore.exceptions.ClientError as e:
            error_code = e.response.get("Error", {}).get("Code")
            if error_code == '404' or error_code == 'NoSuchBucket':
                print(f"{Fore.RED}Error: Specified bucket '{target_bucket_name}' not found.{Style.RESET_ALL}")
            elif error_code == '403' or "AccessDenied" in str(e):
                print(f"{Fore.RED}Error: Access denied to specified bucket '{target_bucket_name}'.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Error accessing specified bucket '{target_bucket_name}': {e}{Style.RESET_ALL}")
            return
    else:
        print(f"{Fore.CYAN}Listing all accessible S3 buckets...{Style.RESET_ALL}")
        try:
            response = s3.list_buckets()
            buckets_to_search = response.get("Buckets", [])
            if not buckets_to_search:
                print(f"{Fore.YELLOW}No buckets found or accessible with profile '{profile}'.{Style.RESET_ALL}")
                return
            print(f"{Fore.CYAN}Found {len(buckets_to_search)} buckets to search.{Style.RESET_ALL}")
        except botocore.exceptions.ClientError as e:
            print(f"{Fore.RED}Error listing buckets: {e}{Style.RESET_ALL}")
            return
        
    start_time = time.time()
    total_objects_scanned = 0
    found_files_details = [] # List of tuples: (bucket, key, url)

    search_criteria_msg = f"Prefix: '{key_prefix_filter}', "
    if exact_file_name:
        search_criteria_msg += f"Exact Name: '{exact_file_name}'"
    elif name_like_pattern:
        search_criteria_msg += f"Pattern (on filename): '*{name_like_pattern}*'" # Clarified pattern target
    print(f"{Fore.CYAN}Searching for files with criteria -> {search_criteria_msg}{Style.RESET_ALL}")

    for bucket_info in buckets_to_search:
        current_bucket_name = bucket_info["Name"]
        print(f"{Fore.BLUE}  Scanning bucket: {current_bucket_name}...{Style.RESET_ALL}")
        try:
            page_count = 0
            for page in paginator.paginate(Bucket=current_bucket_name, Prefix=key_prefix_filter):
                page_count += 1
                if page_count % 10 == 0: # Minor feedback for very large buckets
                    print(f"{Fore.BLUE}    ... still scanning page {page_count} in {current_bucket_name}{Style.RESET_ALL}", end='\r')
                
                for obj in page.get("Contents", []):
                    total_objects_scanned += 1
                    object_key = obj["Key"]
                    
                    if object_key.endswith('/'): 
                        continue # Skip pseudo-directories

                    object_filename = os.path.basename(object_key)
                    matches_criteria = False

                    if name_like_pattern:
                        # Apply pattern to the filename part only
                        if fnmatch.fnmatch(object_filename, f"*{name_like_pattern}*"):
                            matches_criteria = True
                    elif exact_file_name:
                        if object_filename == exact_file_name:
                             matches_criteria = True
                    # If neither --name nor --name-like is given, this function (as per CLI args)
                    # shouldn't find anything because one of them is required by the argparser group.
                    # The CLI definition makes one of these required.

                    if matches_criteria:
                        print(f"{Fore.GREEN}    -> Match found: s3://{current_bucket_name}/{object_key}{Style.RESET_ALL}")
                        try:
                            url = s3.generate_presigned_url(
                                "get_object",
                                Params={"Bucket": current_bucket_name, "Key": object_key},
                                ExpiresIn=3600, # 1 hour
                            )
                            found_files_details.append({
                                "Bucket": current_bucket_name, 
                                "Key": object_key, 
                                "URL": url,
                                "Size": obj.get('Size', 'N/A'),
                                "LastModified": obj.get('LastModified', 'N/A').strftime("%Y-%m-%d %H:%M:%S %Z") if obj.get('LastModified') else 'N/A'
                            })
                        except botocore.exceptions.ClientError as e_presign:
                            print(f"{Fore.YELLOW}      Could not generate presigned URL for {object_key}: {e_presign}{Style.RESET_ALL}")
                            found_files_details.append({
                                "Bucket": current_bucket_name, 
                                "Key": object_key, 
                                "URL": "[Error generating URL]",
                                "Size": obj.get('Size', 'N/A'),
                                "LastModified": obj.get('LastModified', 'N/A').strftime("%Y-%m-%d %H:%M:%S %Z") if obj.get('LastModified') else 'N/A'
                            })
            if page_count > 0 : print(" " * 80, end='\r') # Clear the "still scanning" line

        except botocore.exceptions.ClientError as e_list_obj:
            if "AccessDenied" in str(e_list_obj):
                print(f"{Fore.YELLOW}  Warning: Access Denied when listing objects in bucket '{current_bucket_name}'. Skipping.{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}  Error listing objects in bucket '{current_bucket_name}': {e_list_obj}{Style.RESET_ALL}")
            continue

    end_time = time.time()
    time_taken = end_time - start_time

    if found_files_details:
        print(f"\n{Fore.GREEN}--- Found {len(found_files_details)} matching files ---{Style.RESET_ALL}")
        output_table = PrettyTable()
        output_table.field_names = ["Bucket", "Key", "Size (Bytes)", "Last Modified", "Presigned URL (1hr expiry)"]
        output_table.align = "l"
        output_table.max_width["Key"] = 70
        output_table.max_width["Presigned URL (1hr expiry)"] = 80


        for item in found_files_details:
            output_table.add_row([item["Bucket"], item["Key"], item["Size"], item["LastModified"], item["URL"]])
        print(output_table)
    else:
        print(f"{Fore.YELLOW}\nNo files found matching the specified criteria after scanning {total_objects_scanned} objects.{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Search completed in {time_taken:.2f} seconds. Total objects scanned (approx): {total_objects_scanned}.{Style.RESET_ALL}")