from setuptools import setup, find_packages
setup(
    name="rdsbackup",
    version="0.0.1",
    install_requires=[
        #  It requires these, but it we include them here, it messes with the aws lambda layers for bringing these
        #  libraries into the python environment.  you will need to add these to your local debug environment.
        #boto3,
        #pyodbc,
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': ['add_database_details_to_backup_queue=rdsbackup.Commands.add_database_details_to_backup_queue:script'],
    }
)

