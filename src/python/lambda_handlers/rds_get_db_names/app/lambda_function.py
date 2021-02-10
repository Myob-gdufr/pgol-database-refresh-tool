import json
import pyodbc
from get_secret import get_secret

def lambda_handler(event, context):

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

    # loop over the instance names, get the login secrets, make a connection to the db, and pull the database names from the instance
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
        secret_response = get_secret( secret_key , region)
        secret_string = json.loads(secret_response['SecretString'])

        # set up the connection string
        server = event['body']['db_endpoints'][db_name]['Address']
        username = secret_string['username']
        password = secret_string['password']
        if 'debug' in event:
            print(f'building connection string with server {server} and username {username}')
        conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + str(server) + ';UID=' + str(username) + ';PWD=' + str(password)

        db_connection = pyodbc.connect(conn_str)
        cursor = db_connection.cursor()
        cursor.execute('select [name] as database_name from sys.databases order by name')
        db_list[db_name]['databases'] = []
        for row in cursor.fetchall():
            if 'debug' in event:
                print(f'got db {row[0]} in instance {db_name}')
            db_list[db_name]['databases'].append(row[0])

    return {
        'statusCode': 200,
        'body': json.dumps(db_list, default=str)
    }
