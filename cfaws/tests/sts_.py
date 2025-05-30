import boto3 as b
import os

def get_mfa_serial():
    iam_client = b.client('iam')
    sts_client = b.client('sts')
    caller_identity = sts_client.get_caller_identity()
    username = caller_identity['Arn'].split('/')[-1]

    mfa_device = iam_client.list_mfa_devices(UserName=username)
    if not mfa_device['MFADevices']:
        print("\033[91mError: No MFA device found for user.\033[0m")
        

    return mfa_device['MFADevices'][0]['SerialNumber']

def get_cli_admin_role_arn():
    iam_client = b.client('iam')
    roles = iam_client.list_roles()
    
    for role in roles['Roles']:
        if role['RoleName'] == 'CLI_ADMIN':
            #print(f"role arn: {role['Arn']}")
            return role['Arn']

    # If role wasn't found after the loop, print the error and return None
    print("\033[91mError: CLI_ADMIN role not found.\033[0m")
    

mfa_serial = get_mfa_serial()
if mfa_serial:
    print(mfa_serial)
else: 
    exit(1)

role_arn = get_cli_admin_role_arn()
if role_arn:
    print(role_arn)
else:
    exit(1)


def assume_role_with_mfa(role_arn, mfa_serial, session_name="CLI_Admin_Session"):
    sts_client = b.client('sts')
    mfa_token = input("Enter your MFA token: ")

    try:
        assumed_role_object = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName=session_name,
            SerialNumber=mfa_serial,
            TokenCode=mfa_token
        )
        credentials= assumed_role_object['Credentials']
        return credentials
    except Exception as e:
        print("\033[91mError assuming role: {}\033[0m".format(e))
        exit(1)
    
def main():
    MFA_SERIAL = get_mfa_serial()
    ROLE_ARN = get_cli_admin_role_arn()

    
    credentials = assume_role_with_mfa(ROLE_ARN, MFA_SERIAL)
    print(credentials)

#### THIS ONLY WORKS IF YOU WANT THE SCRIPT TO DO SOMETHING ELSE. IT WILL NOT PASS IT TO YOUR LOCAL TERMINAL ###
    # os.environ['AWS_ACCESS_KEY_ID'] = credentials['AccessKeyId']
    # os.environ['AWS_SECRET_ACCESS_KEY'] = credentials['SecretAccessKey']
    # os.environ['AWS_SESSION_TOKEN'] = credentials['SessionToken']

    token_object = {
        "aws_access_key_id": credentials["AccessKeyId"],
        "aws_secret_access_key": credentials["SecretAccessKey"],
        "aws_session_token": credentials["SessionToken"]
        }

    
    for key, value in token_object.items():
            print(f"aws --profile temp-token configure set {key} {value}")
            os.system(f"aws --profile temp-token configure set {key} {value}")
    print(f"aws --profile temp-token configure set region us-gov-west-1")
    os.system(f"aws --profile temp-token configure set region us-gov-west-1")
    print()
    print("\033[92mSuccessfully appended the profile as temp-token!\033[0m")
    print()
    print("\033[92m Setting the profile as temp-token! \033[0m")
    os.system('osascript -e \'tell app "Terminal" to do script "export AWS_PROFILE=temp-token"\'')
    
    

if __name__ == "__main__":
  main()
    
