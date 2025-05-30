import boto3
import json
import csv
import re
import os, time



#os.chdir("C:\\Users\\JumpAdmin\\Documents\\Automation\\Forescout - Inventory")
# Client specific information - needs to be changed on a per client basis
domain_name = "forescoutdomain"
net_bios = "netbios"
operating_region = "us-gov-west-1"
client_name = "forescout"
accounts = ['fc-mgmt','fc-app']  
# do not change - creates file for data to be dumped into.
inventoryfile = open(client_name + '_inventory.csv', "w")
# Clean ec2_data to proper json formatting
def clean_data(data, to_print):
    str_data = str(data)
    str_data = str_data.replace('\'', '\"')
    str_data = str_data.replace('True', '"True"')
    str_data = str_data.replace('False', '"False"')
    str_data = str_data.replace('""True""', '"True"')
    str_data = str_data.replace('""False""', '"False"')
    str_data = str_data.replace('datetime.datetime', '"datetime.datetime')
    str_data = str_data.replace('))', '))"')
    str_data = re.sub('/"LaunchTime":.+, /', '', str_data)
    parsed_data = json.loads(str_data)
    if to_print:
        print(json.dumps(parsed_data, indent=4, sort_keys=False))
    return parsed_data
def checkTrue(val):
    if val == "1":
        return "Pass"
    else:
        return "Fail"
    
def merge_dictionaries(dict1: dict, dict2: dict):
    new_dict = dict1 | dict2
    return new_dict

def getEC2():
    debug = False

    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls

    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        ec2_resource = session.client('ec2')
        # Pull and clean ec2_data from AWS
        ec2_data = ec2_resource.describe_instances()
        # print(ec2_data)
        # Print IP Address of each Instance
        with open(client_name + '_inventory.csv', 'a') as outputfile:
            writer = csv.writer(outputfile, delimiter='\t', lineterminator='\n', )
            for ec2_instance in ec2_data['Reservations']:
                name = "-"
                os = "-"
                is_public = "No"
                instanceId = ""
                privateIp = ""
                if (ec2_instance['Instances'][0]):
                    instanceId = ec2_instance['Instances'][0]['InstanceId']
                    privateIp = ec2_instance['Instances'][0]['PrivateIpAddress'].strip()
                    if ("Tags" in ec2_instance['Instances'][0].keys()):
                        for tag in ec2_instance['Instances'][0]['Tags']:
                            if (tag['Key'] == 'Name'):
                                name = tag['Value'] + "." + domain_name
                            if (tag['Key'] == 'OSFamily'):
                                os = tag['Value']
                    if (ec2_instance['Instances'][0]['NetworkInterfaces']):
                        for eni in ec2_instance['Instances'][0]['NetworkInterfaces']:
                            if ("Association" in eni.keys()):
                                if ("PublicIp" in eni['Association'].keys()):
                                    is_public = "Yes"
                else:
                    name = "Failed to gather"
                    os = "Failed to gather"
                    instanceId = "Failed to gather"
                    privateIp = "Failed to gather"
                lineout = str(instanceId + "," + privateIp + "," + "Yes" + "," + is_public + "," + name.strip() + "," + net_bios + ",,Yes,," + os + "," + operating_region + ",,AWS EC2,,,,,,,,," + client_name)
                row = [lineout]
                writer.writerow(row)
def getELBv1_DNSName(elbv1_name: str):
    elbv1_dict = {}
    elbv1_list = []
    elbv1_list.append(elbv1_name)
    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        elbv1_resource = session.client('elb')
        # Pull and clean ec2_data from AWS
        elbv1_data = elbv1_resource.describe_load_balancers(
            LoadBalancerNames=elbv1_list
        )
        if (elbv1_data['LoadBalancerDescriptions']):
            for elb in elbv1_data['LoadBalancerDescriptions']:
                name = elb['LoadBalancerName']
                dns_name = elb['DNSName']
                # print(name,dns_name)
                elbv1_dict[name] = {}
                elbv1_dict[name]['DNSName'] = dns_name
                # print(elbv2_dict)
                return dns_name
        else:
            return "Failed to gather"


def getELBs():
    debug = False

    elbv2_dict = {}
    eni_dict = {}

    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        elbv2_resource = session.client('elbv2')

        # Pull and clean ec2_data from AWS
        elbv2_data = elbv2_resource.describe_load_balancers()
        # print(elbv2_data)

        # Collect ELB Names and DNS Names
        if (elbv2_data['LoadBalancers']):
            for elb in elbv2_data['LoadBalancers']:
                name = elb['LoadBalancerName']
                dns_name = elb['DNSName']
                elb_type = elb['Type']
                # print(name,dns_name,elb_type)

                elbv2_dict[name] = {}
                elbv2_dict[name]['DNSName'] = dns_name
                elbv2_dict[name]["Type"] = elb_type
                # print(elbv2_dict)

        #  ENI Information
        eni_resource = session.client('ec2')
        elbv2_eni_data = eni_resource.describe_network_interfaces(
            Filters=[
                {
                    'Name': 'description',
                    'Values': [
                        'ELB *'
                    ]
                }
            ]
        )
        # print(elbv2_eni_data)

        #  Clean ENI IP List

        if (elbv2_eni_data['NetworkInterfaces']):
            for eni in elbv2_eni_data['NetworkInterfaces']:
                #  Get attached ELB Name and store it after cleaning it to match the actual name of the ELB
                # REGEX here can break all the things - caution is advised.+
                #name_uncleaned2 = re.search(
                #    r"(?:ELB\s\w{3}\/|ELB\s)((\w+\-)+(alb|nlb|\w+)|(\w+\-|asa)+(alb|nlb|(?:asa)nlb))",
                #    name_uncleaned)
                #name_uncleaned3 = re.search(r"(?:ELB\s\w{3}\/|ELB\s)(.*)", name_uncleaned2)

                name_uncleaned = eni["Description"]
                #print (name_uncleaned)
                name_uncleaned2 = re.search(r"(?:ELB\s\w{3}\/|ELB\s)(.*)\/(?:.*)", name_uncleaned)
                print (name_uncleaned2.group(1))
                elb_name = name_uncleaned2.group(1)

                #  Get the IP of the ENI
                if (eni["PrivateIpAddresses"][0]["PrivateIpAddress"]):
                    elb_eni_ip = eni["PrivateIpAddresses"][0]["PrivateIpAddress"]
                    print(elb_eni_ip)
                else:
                    elb_eni_ip = "Failed to gather"

                #  Check if the ENI is Public
                if ("Association" in eni.keys()):
                    if ("PublicIp" in eni['Association'].keys()):
                        is_public = "Yes"
                    elif ("PublicIp" not in eni['Association'].keys()):
                        is_public = "No"

                elif ("Association" not in eni.keys()):
                    is_public = "No"

                #  Get the Location of the ENI (Region and AZ)
                if (eni["AvailabilityZone"]):
                    avail_zone = eni["AvailabilityZone"]

                region = re.search(r"(.*\-\d)", avail_zone).group(0)
                # print(region)

                #  Create the Dictionary for ELBs with the details
                #    If the ELB is already in the list, simply add additional IPs from additional ENIs
                if elb_name in eni_dict:
                    # print(elb_name, " is already in the list... adding additional IPs.")
                    if (eni_dict[elb_name]["IpAddresses"]):
                        eni_dict[elb_name]["IpAddresses"].append(elb_eni_ip)
                        eni_dict[elb_name]["IsPublic"] = is_public

                #  If the ELB is not in the list, do first time setup and add it
                else:
                    # print("Not in the list - adding an ELB named: ", elb_name)
                    eni_dict[elb_name] = {}
                    eni_dict[elb_name]["IpAddresses"] = []
                    eni_dict[elb_name]["IpAddresses"].append(elb_eni_ip)
                    if (elb_name in elbv2_dict):
                        eni_dict[elb_name]["DNSName"] = elbv2_dict[elb_name]["DNSName"]
                        eni_dict[elb_name]["Type"] = elbv2_dict[elb_name]["Type"]
                        # print(eni_dict[elb_name])
                    eni_dict[elb_name]["IsPublic"] = is_public
                    eni_dict[elb_name]["AvailabilityZone"] = avail_zone
                    eni_dict[elb_name]["Region"] = region
        else:
            elb_name = "Failed to gather"
            elb_eni_ip = "Failed to gather"
            is_public = "Failed to gather"
            avail_zone = "Failed to gather"
            region = "Failed to gather"

        #  If the ENI is for an ELBv1 - populate the info accordingly and print to CSV
        #    - Match the current ELB being iterated and append the IPs for it to the ELB List
        with open(client_name + '_inventory.csv', 'a') as outputfile:
            writer = csv.writer(outputfile, delimiter='\t', lineterminator='\n', )
            for elb, elb_info in eni_dict.items():
                if ("DNSName" not in elb_info):
                    eni_dict[elb]["DNSName"] = getELBv1_DNSName(elb)
                if ("Type" not in elb_info):
                    eni_dict[elb]["Type"] = "classic"

                #  Print each ELB as a CSV-formatted String
                ipaddresses_str = ";".join(eni_dict[elb]["IpAddresses"])
                # print(elb + "," + ipaddresses_str + ",Yes," + eni_dict[elb]["IsPublic"] + "," + eni_dict[elb]["DNSName"] + ",,,No,,," + eni_dict[elb]["Region"] + ",ELB," + eni_dict[elb]["Type"] + ",,,,,,,,," + client_name)
                lineout = str(elb + "," + ipaddresses_str + ",Yes," + eni_dict[elb]["IsPublic"] + "," + eni_dict[elb][
                    "DNSName"] + ",,,No,,," + eni_dict[elb]["Region"] + ",ELB," + eni_dict[elb][
                                  "Type"] + ",,,,,,,,," + client_name)
                row = [lineout]
                writer.writerow(row)

                # print(eni_dict)


def getRDS():
    debug = False

    for acct in accounts:
        session = boto3.Session(profile_name=acct)
        rds_resource = session.client('rds')

        rds_data = rds_resource.describe_db_instances()

        # print(rds_data)
        with open('inventory.csv', 'a') as outputfile:
            writer = csv.writer(outputfile, delimiter='\t', lineterminator='\n', )
            for rds_instance in rds_data['DBInstances']:
                # print(rds_instance['DBInstanceIdentifier'] + ",,Yes," + str(rds_instance['PubliclyAccessible']) + "," + rds_instance['Endpoint']['Address'] + ",,,,,,,,,," + rds_instance['Engine'] + "," + rds_instance['EngineVersion'] + ",," + rds_instance['DBInstanceIdentifier'] + ",,,," + client_name)
                lineout = str(
                    rds_instance['DBInstanceIdentifier'] + ",,Yes," + str(rds_instance['PubliclyAccessible']) + "," +
                    rds_instance['Endpoint']['Address'] + ",,,,,,,,,," + rds_instance['Engine'] + "," + rds_instance[
                        'EngineVersion'] + ",," + rds_instance['DBInstanceIdentifier'] + ",,,," + client_name)
                row = [lineout]
                writer.writerow(row)


getEC2()
getRDS()
getELBs()

def cleanup():
# Cleans up temp file created during inventory creation.
    if os.path.exists(client_name + '_inventory.csv'):
        os.remove(client_name + '_inventory.csv')
    else:
        print("The file does not exist")

# cleaning up duplicated lines from ELB list build
inFile = open(client_name + '_inventory.csv', 'r')
outFile = open(client_name + '_final_inventory.csv', 'w')
listLines = []
for line in inFile:
    if line in listLines:
        continue
    else:
        outFile.write(line)
        listLines.append(line)
outFile.close()
inFile.close()

#cleanup()