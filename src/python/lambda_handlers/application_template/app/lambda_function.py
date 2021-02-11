import json
import pyodbc
from get_secret import get_secret

### This file demonstrates a lambda handler function
### It's primary purpose is to receive a request and provide a properly formatted response
### all code paths must provide a properly formatted reponse

def lambda_handler(event, context):

    ### handle the inputs
    db_list = {}
    if 'body' in event:
        if 'db_endpoints' in event['body']:
            db_endpoints = event['body']['db_endpoints']
            if 'debug' in event:
                print(f'received db_list {db_endpoints}')
    else:
        example_event = {
            "statusCode": 200,
            "debug": 1,
            "body": {
                "db_endpoints": {
                    "RDS-002t": {
                        "Address": "rpuqa8yeaij86q.crqxd7hsfi2c.ap-southeast-2.rds.amazonaws.com",
                        "Port": 1433,
                        "HostedZoneId": "Z32T0VRHXEXS0V"
                    }
                }
            }
        }
        return {
            "statusCode": 400,
            "message": "required parameter missing: db_endpoints",
            "expected structure": f"array of db names and endpoints e.g. {example_event}"
        }

    ### loop over the instance names, get the login secrets, make a connection to the db, and pull the database names from the instance
    for db_name in event['body']['db_endpoints']:
        if 'debug' in event:
            print(f'looping over db_name {db_name}')

        #initialize the return object
        db_list[db_name] = {}
        # put the endpoint in the return object
        db_list[db_name]['endpoint'] = event['body']['db_endpoints'][db_name]
        region = "ap-southeast-2"

        # a hack to set the secret prefix since they're different in different accounts, will only work in test and prod
        secret_key = "RDS-Admin-Secret-PayGlobalOnline-" + db_name
        if db_name == 'RDS-002t':
            secret_key = 'RDS-Admin-Secret-Test-PayGlobalOnline-' + db_name

        if 'debug' in event:
            print(f'pulling secrets for {secret_key}')
        try:
            secret_response = get_secret( secret_key, region)
        except:
            return{
                "statusCode": 500,
                "message": "unable to get login info from secretsmanager"
            }
        secret_string = json.loads(secret_response['SecretString'])

        # set up the connection string, run the query, and handle the result 
        # should move this db interaction stuff into a dedicated module
        server = event['body']['db_endpoints'][db_name]['Address']
        username = secret_string['username']
        password = secret_string['password']
        if 'debug' in event:
            print(f'building connection string with server {server} and username {username}')
        conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + str(server) + ';UID=' + str(username) + ';PWD=' + str(password)

        try:
            db_connection = pyodbc.connect(conn_str)
        except:
            return {
                "statusCode": 500,
                "message": "unable to get connect to db"
            }
        cursor = db_connection.cursor()

        try:
            cursor.execute('select [name] as database_name from sys.databases order by name')
        except:
            return {
                "statusCode": 500,
                "message": "unable to execute sql query"
            }
            
        db_list[db_name]['databases'] = []
        for row in cursor.fetchall():
            if 'debug' in event:
                print(f'got db {row[0]} in instance {db_name}')
            db_list[db_name]['databases'].append(row[0])

    return {
        'statusCode': 200,
        'body': json.dumps(db_list, default=str)
    }

#Allows lambda_handler to the called/tested from the command line, defaults to the 'test' aws profile
def script():
    import argparse

    # handle the input parameters
    parser = argparse.ArgumentParser(description='describe the db instances in an account in a region')
    parser.add_argument('--profile', dest='profile', help='The aws profile to use for the request', default='test')
    parser.add_argument('--body', dest='body', help='The request body to test', default={})
    args = parser.parse_args()

    # initialize the event with the expected parameters
    event = {
        "statusCode": 200,
        "debug": 1,
    }
    # add the passed in parameters to the event
    for (k,v) in args.items():
        event[k] = v    
    
    # call the lambda handler, pass the parameters, and return the result
    result = lambda_handler(event, {})
    return result

if __name__ == '__main__':
    script()
