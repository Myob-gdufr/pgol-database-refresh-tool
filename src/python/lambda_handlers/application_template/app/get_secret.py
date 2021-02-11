import boto3
import base64
from botocore.exceptions import ClientError

### This file demonstrates an implementation of AWS API interaction using the boto3 library
### refer to the boto3 docs for a list of available services and detailed information about each
###
### https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html

# based on example from the AWS docs:   
# https://aws.amazon.com/developers/getting-started/python/
def get_secret(secret_name, region_name):

    # Create a Secrets Manager client
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    except e:
        raise e

    #initialize the response
    get_secret_value_response = {}

    # call the desired secrestsmanager function  
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    
    if 'SecretString' in get_secret_value_response:
        return get_secret_value_response
    else:
        return "no secret value response"
    