import boto3
import string
import random
from botocore.exceptions import NoCredentialsError, ClientError

def iam_change_user_password(args):

    profile = args.profile
    region = args.region
    user_name = args.user

    # Create a session
    session = boto3.Session(profile_name=profile, region_name=region)

    # Create an IAM resource from that session
    iam = session.client('iam')

    # Generate a new password
    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(secrets.choice(alphabet) for _ in range(10))  # for a 10-character password

    try:
        response = iam.update_login_profile(
            UserName=user_name,
            Password=new_password,
            PasswordResetRequired=True
        )
        print(f"The new password for {user_name} is: {new_password}")

    except iam.exceptions.NoSuchEntityException:
        print("The specified user does not have a password. Creating one.")
        response = iam.create_login_profile(
            UserName=user_name,
            Password=new_password,
            PasswordResetRequired=False
        )
        print(f"The password for {user_name} is: {new_password}")
    except Exception as e:
        print(f"An error occurred: {e}")

