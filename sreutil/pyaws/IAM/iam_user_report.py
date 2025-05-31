import boto3
import json
from prettytable import PrettyTable
import csv
import datetime
import textwrap

def iam_user_report(args):
    session = boto3.Session(
        region_name=args.region,
        profile_name=args.profile
    )
    client = session.client('iam')

    # Generate the IAM credential report
    response = client.generate_credential_report()
    state = response['State']

    # Wait for the report to be generated
    while state != 'COMPLETE':
        response = client.generate_credential_report()
        state = response['State']

    # Get the credential report in text format
    response = client.get_credential_report()
    report_text = response['Content'].decode('utf-8')

    # Split the report into lines and extract the header and user information
    header, *user_lines, footer = report_text.split('\n')

    # Create prettytable and set its field names
    x = PrettyTable()
    header_fields = header.split(',')
    x.field_names = header_fields

    # Add users' information to the table
    for user_line in user_lines:
        user_fields = user_line.split(',')
        wrapped_fields = [ '\n'.join(textwrap.wrap(field, width=200)) for field in user_fields ]
        x.add_row(wrapped_fields)

    # Print the table
    print(x)

    # Check if CSV path is provided
    if args.csv_path:
        with open(args.csv_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row to the file
            writer.writerow(header_fields)

            # Write the rows to the file
            for user_line in user_lines:
                user_fields = user_line.split(',')
                writer.writerow(user_fields)

        print('IAM credential report exported to {}'.format(args.csv_path))
