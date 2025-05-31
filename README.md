# CFAWS

`cfaws` is a command-line tool for querying and managing various AWS resources, such as EC2 instances, RDS instances, IAM users, security groups, and more.

## Features

- Retrieve information about EC2 instances
- List RDS versions
- Get security group details
- (look at the man page with cfaws man for more)

## Installation With Script (Virtual Env -- RECOMMENDED)

1. Clone this repository:
2. Change to the `cfaws` directory:
3. Run `./setup.sh`
4. Open a new terminal session and run `cfaws man` to get an output and test functionality



## Manual Installation with Python Set Up ##
1. Clone this repository:
2. Change to the `cfaws` directory:
3. Install the required Python packages: 
4. Install the `cfaws` package: From the cfaws directory, run pip install -e .
5. Open a new terminal session and run `cfaws man` to get an output and test functionality


## Usage
To use `cfaws`, run the following command with the appropriate arguments:

Replace `<subcommand>` with the desired action (e.g., `ec2-details`, `sg-details`, etc.), and `[options]` with the necessary flags and parameters.

For a full list of subcommands and options, run: cfaws --help
For a list of supported arguments for the subcommands, run: cfaws `<subcommand>` -h


## Examples

- Get EC2 instance details:
   cfaws ec2-details --profile your-aws-profile --region your-region --name instance-name
- Get EC2 instance details help: cfaws ec2-details -h









