import boto3
import csv
from prettytable import PrettyTable as pretty

def rds_versions(profile_name, region_name, output_file=""):
    region = region_name
    endpoint_url = 'https://rds.us-gov-west-1.amazonaws.com'

    session = boto3.Session(
        region_name='us-gov-west-1',
        profile_name=profile_name
    )

    # create RDS client
    rds = session.client('rds')

    # get all DB instances
    db_instances = rds.describe_db_instances()
    
    data_rows = []
    
    with open('rds_version_check.csv', mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write header row
        writer.writerow(['database name', 'db_engine', 'Current Version', 'Message'])

        for db_instance in db_instances['DBInstances']:
            db_instance_id = db_instance['DBInstanceIdentifier']
            db_engine = db_instance['Engine']
            db_engine_version = db_instance['EngineVersion']
            db_engine_major_version = db_engine_version.split('.')[0]
            db_engine_minor_version = db_engine_version.split('.')[1]

            # get available engine versions
            available_versions = rds.describe_db_engine_versions(
                Engine=db_engine,
                EngineVersion=db_engine_major_version
            )

            # check if there is a newer minor version available
            newer_version = None
            table = pretty(['Database Name', 'Engine Flavor', 'Higher Version Available?', 'Current Version', 'Latest Version'])
            for version in available_versions['DBEngineVersions']:
                if int(version['EngineVersion'].split('.')[1]) > int(db_engine_minor_version):
                    newer_version = version['EngineVersion']
                    break

            # print result
            if newer_version:
              #version_message = f"{db_instance_id} has a newer version available, {newer_version}. | Current version: {db_engine_version}"
              #print(version_message)
              message = "YES"
              table.add_row([db_instance_id, db_engine, message, db_engine_version, newer_version])
            else:
              #version_message = f"{db_instance_id} is on the latest version, {db_engine_version}. | Current version: {db_engine_version}"
              message = "NO"
              table.add_row([db_instance_id, db_engine, message, db_engine_version, db_engine_version])


              
              
            # Write Teh Data
            print(table)
            writer.writerow([db_instance_id, db_engine, db_engine_version, message ])