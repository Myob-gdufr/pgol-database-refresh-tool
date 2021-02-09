import json
import pyodbc
from get_secret import get_secret

def lambda_handler(event, context):

    db_list = {}
    if 'db_names' in event:
        if 'debug' in event:
            received_names = event['db_names']
            print(f'received db_list {received_names}')
    else:
        example_request = "{\"db_names\": [\"camel\", \"bear\", \"aardvark\"], \"db_endpoints\": {\"camel\": {\"Address\": \"rp15sh7qh7q3u4v.cq5ljoh1cbwr.ap-southeast-2.rds.amazonaws.com\", \"Port\": 1433, \"HostedZoneId\": \"Z32T0VRHXEXS0V\"}, \"bear\": {\"Address\": \"rpoa8aqv9pka4o.cq5ljoh1cbwr.ap-southeast-2.rds.amazonaws.com\", \"Port\": 1433, \"HostedZoneId\": \"Z32T0VRHXEXS0V\"}, \"aardvark\": {\"Address\": \"rpr8vzhnsqc2wz.cq5ljoh1cbwr.ap-southeast-2.rds.amazonaws.com\", \"Port\": 1433, \"HostedZoneId\": \"Z32T0VRHXEXS0V\"}}}"
        return {
            "statusCode": 400,
            "message": "required parameter missing: db_list",
            "expected structure": f"array of db names and endpoints e.g. {example_request}"
        }

    # loop over the instance names, get the login secrets, make a connection to the db, and pull the database names from the instance
    for db_name in event['db_names']:
        if 'debug' in event:
            print(f'looping over db_name {db_name}')
        db_list[db_name] = {}
        region = "ap-southeast-2"

        # This might be doing too much in a single function. Maybe better to break get_secret into its own function? 
        # except that passing secrets around wouldn't be secure so I'll do it here (in the place where they're used)
        if 'debug' in event:
            print(f'pulling secrets for RDS-Admin-Secret-PayGlobalOnline-{db_name}')
        secret_response = get_secret("RDS-Admin-Secret-PayGlobalOnline-"+db_name , region)
        secret_string = json.loads(secret_response['SecretString'])

        # set up the connection string
        server = event['db_endpoints'][db_name]['Address']
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
