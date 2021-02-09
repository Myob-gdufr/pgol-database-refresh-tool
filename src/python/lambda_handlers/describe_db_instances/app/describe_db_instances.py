import boto3
from botocore.exceptions import ClientError

def describe_db_instances(region_name="ap-southeast-2"):
    
    # Create an RDS client
    session = boto3.session.Session()
    client = session.client(
        service_name='rds',
        region_name=region_name
    )

    try:
        response = client.describe_db_instances()
    except ClientError as e:
        raise e        
        
    return response