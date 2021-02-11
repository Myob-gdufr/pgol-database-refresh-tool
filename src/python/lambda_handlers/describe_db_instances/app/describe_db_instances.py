import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

def describe_db_instances( *kwargs ):

    if kwargs:
        profile = kwargs[0].get('profile')
    else:
        profile = ''
    
    try:
        if profile:
            session = boto3.session.Session(profile_name=profile)
        else:
            session = boto3.session.Session()

        client = session.client(service_name='rds', region_name='ap-southeast-2')        

        response = client.describe_db_instances()

    except Exception as e:
        print(e)
        raise e        
        
    return response