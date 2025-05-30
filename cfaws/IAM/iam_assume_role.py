import boto3 as b
import os

def get_mfa_serial(args):
    profile = args.profile
    region = args.region


    session = b.Session(profile_name=profile, region_name=region)

    iam_client = session.client('iam')
    sts_client = session.client('sts')
    caller_identity = sts_client.get_caller_identity()
    username = caller_identity['Arn'].split('/')[-1]

    mfa_device = iam_client.list_mfa_devices(UserName=username)
    if not mfa_device['MFADevices']:
        print("\033[91mError: No MFA device found for user.\033[0m")
        

    return mfa_device['MFADevices'][0]['SerialNumber']

def get_cli_admin_role_arn(args):

    profile = args.profile
    region = args.region


    session = b.Session(profile_name=profile, region_name=region)

    iam_client = session.client('iam')
    roles = iam_client.list_roles()
    
    for role in roles['Roles']:
        if role['RoleName'] == 'CLI_ADMIN':
            #print(f"role arn: {role['Arn']}")
            return role['Arn']

    # If role wasn't found after the loop, print the error and return None
    print("\033[91mError: CLI_ADMIN role not found.\033[0m")
    


def assume_role_with_mfa(args,role_arn, mfa_serial, session_name="CLI_Admin_Session"):

    profile = args.profile
    region = args.region
    token = args.token

    session = b.Session(profile_name=profile, region_name=region)

    sts_client = session.client('sts')
    mfa_token = token

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
    
def iam_set_role(args):
    profile = args.profile
    region = args.region

    MFA_SERIAL = get_mfa_serial(args)
    ROLE_ARN = get_cli_admin_role_arn(args)

    if not MFA_SERIAL or not ROLE_ARN:
        exit(1)

    
    credentials = assume_role_with_mfa(args, ROLE_ARN, MFA_SERIAL)


    token_object = {
        "aws_access_key_id": credentials["AccessKeyId"],
        "aws_secret_access_key": credentials["SecretAccessKey"],
        "aws_session_token": credentials["SessionToken"]
        }

    
    for key, value in token_object.items():
            #The line below prints the credentials to the assumed role. Don't uncomment unless you want to output those
            #print(f"aws --profile {profile}-temp! configure set {key} {value}")
            print(f"Configuring AWS Profile, {profile}-temp! configure set {key}")
            os.system(f"aws --profile {profile}-temp! configure set {key} {value}")

    print(f"aws --profile {profile}-temp! configure set region us-gov-west-1")
    os.system(f"aws --profile {profile}-temp! configure set region {region}")

    if os.name == 'nt':  # Windows
        print(f"\033[92mWindowsOS Detected (gross)...launching new windows terminal\033[0m")
        print(f"\033[92m Setting the profile as {profile}-temp! in NEW TERMINAL \033[0m")
        os.system(f'start cmd /k "set AWS_PROFILE={profile}-temp!"')
    elif os.name == 'posix' and os.uname().sysname == 'Darwin':  # MacOS
        print(f"\033[92mMacOS Detected\033[0m")
        print(f"\033[92mSetting the profile as {profile}-temp! in NEW TERMINAL \033[0m")
        os.system(f'osascript -e \'tell app "Terminal" to do script "export AWS_PROFILE={profile}-temp!"\'')
    else:
        print("\033[91mThis OS is not supported for opening a new terminal with the set profile. Please manually set the AWS_PROFILE.\033[0m")