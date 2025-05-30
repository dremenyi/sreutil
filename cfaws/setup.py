from setuptools import setup, find_packages

setup(
    name='cfaws',
    version='0.0.7',
    packages=find_packages(),
    py_modules=['cf_aws_cli'],
    install_requires=[
        'boto3',
        'colorama',
        'prettytable',
        'pandas',
        
    ],
    entry_points={
        'console_scripts': [
            'cfaws = cf_aws_cli:main',
        ],
    },
)
