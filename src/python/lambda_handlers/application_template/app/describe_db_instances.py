import boto3
from botocore.exceptions import ClientError
from botocore.config import Config

### This file demonstrates an implementation of AWS API interaction using the boto3 library
### refer to the boto3 docs for a list of available services and detailed information about each
###
### https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html

# this function does not require any parameters for execution as a lambdad function
# *kwargs is only used when executing locally
def describe_db_instances( *kwargs ):

    # when called from the command line, use the configured aws profile. default: test (see the lambda_function.py "script()" function)
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
