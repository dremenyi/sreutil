SRE Utility Toolkit (sreutil)
sreutil is a command-line toolkit designed for Site Reliability Engineers (SREs) and cloud operations personnel to streamline and automate common administrative tasks. Its primary component, pyaws, provides a powerful and efficient interface for managing a wide range of AWS resources, consolidating many frequent operations into a single, consistent tool.

Key Features
The pyaws sub-tool is engineered for faster operations by optimizing API calls, automating multi-step processes, and simplifying secure access.

EC2 Instance Management:

Rapid Inventory and Status Checks: Quickly get a detailed inventory of all EC2 instances, including their status, IDs, IP addresses, and associated subnet/VPC information (ec2-inventory, ec2-details).

Lifecycle Operations: Start and stop instances directly from the command line (ec2-start-stop).

Disaster Recovery and Maintenance: Automate the creation of snapshots for root volumes (ec2-create-snapshot) and efficiently replace an instance's root volume from a snapshot or AMI for quick rollbacks or gold image deployments (ec2-replace-root-volume).

Secure Remote Access:

SSM Integration: Leverage AWS Systems Manager (SSM) to provide secure, auditable access to instances without requiring open SSH or RDP ports on security groups.

Encrypted Tunneling: Initiate interactive shell sessions (ec2-start-session) or set up port forwarding for RDP or web console access (ec2-port-forward) over a secure, FIPS 140-2 validated tunnel.

S3 and Secrets Management:

Efficiently list buckets and objects (s3-list-buckets, s3-list-files), and find specific files across all buckets with pattern matching (s3-find-file).

Securely list and retrieve secrets from AWS Secrets Manager, with options to mask sensitive values by default (sm-list-secrets, sm-get-secret).

IAM and Security Auditing:

Perform security audits on IAM users, checking for MFA, access key age, and permissions (iam-audit).

Manage IAM user credentials, including key rotation and password changes (iam-rotate-key, iam-change-user-password).

Installation
Prerequisites
Python 3.8+

pip

Configured AWS credentials (e.g., via aws configure or environment variables).

Steps
Clone the Repository:

git clone <your-repository-url>
cd sreutil  # Or your repository's root folder name

Install Dependencies and the Tool:
It is highly recommended to install the tool in a Python virtual environment.

# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install the package in editable mode
pip install -e .

The -e flag installs the package in "editable" mode, which means changes you make to the source code will immediately be available without needing to reinstall.

Usage
The tool uses a tool -> command structure. The main tool currently available is pyaws.

Command Structure
sreutil <tool> <command> [options]

General Help
To see the list of available tools, run:

sreutil -h

To see the detailed manual for the pyaws tool, including all its commands:

sreutil pyaws man

To get help for a specific pyaws command:

sreutil pyaws <command> -h

Examples
Get an inventory of all EC2 instances:

sreutil pyaws ec2-inventory --profile your-dev-profile --region us-east-1

Get details for a specific instance:

sreutil pyaws ec2-details --profile your-dev-profile --name "web-server-01"

Create a snapshot of an instance's root volume and wait for it to complete:

sreutil pyaws ec2-create-snapshot --profile your-prod-profile --name "database-main" --show-progress

Start a secure shell session into an instance via SSM:

sreutil pyaws ec2-start-session --profile your-prod-profile --name "bastion-host"

Find a file in S3 and get a presigned URL:

sreutil pyaws s3-find-file --profile your-data-profile --name-like "*.csv.gz" --key "data/2024/"

List secrets but hide the values:

sreutil pyaws sm-list-secrets --profile your-sec-profile

List secrets AND show the values (use with caution):

sreutil pyaws sm-list-secrets --profile your-sec-profile --show-values

Development
To contribute, clone the repository and install in editable mode as described above. Ensure any new functionality includes appropriate argument parsing in sreutil/sreutil_cli.py and follows the existing modular structure.

License
This project is licensed under the MIT License - see the LICENSE file for details.