import boto3
import os

def s3_download_file(profile, bucket, key, output_dir):
    
      session = boto3.Session(region_name='us-gov-west-1', profile_name=profile)

      s3 = session.resource('s3')
      bucket = s3.Bucket(bucket)
      
      for obj in bucket.objects.filter(Prefix=key):
            if obj.key.endswith('/'):  # ignore directories
                continue
            file_path = os.path.join(os.getcwd(), obj.key)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            bucket.download_file(obj.key, file_path)