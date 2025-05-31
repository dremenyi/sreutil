# from setuptools import setup, find_packages

# setup(
#     name='sreutil',
#     version='1.0.0',
#     packages=find_packages(),
#     py_modules=['sreutil_cli'],
#     install_requires=[
#         'boto3',
#         'colorama',
#         'prettytable',
#         'pandas',
        
#     ],
#     entry_points={
#         'console_scripts': [
#             'sreutil = sreutil_cli:main',
#         ],
#     },
# )


from setuptools import setup, find_packages

setup(
    name='sreutil',
    version='0.1.0', # Start fresh
    packages=find_packages(where='.'), # Tells setuptools to look for packages in the current dir
                                     # and it should find the 'sreutil' package.
    # Or, if your structure is sreutil_repo_root/sreutil_package_dir
    # packages=find_packages(),
    # package_dir={'': '.'}, # if sreutil (package) is at the root
    install_requires=[
        'boto3',
        'colorama',
        'prettytable',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'sreutil = sreutil.sreutil_cli:main', # Points to main in sreutil/sreutil/cli.py
        ],
    },
)