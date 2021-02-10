import json
from describe_db_instances import describe_db_instances

# by default return the whole describe_db_instances response and let the caller decide what they want out of it
# if event[name_list], return the name list as an array
# if event[endpoint_list], return the endpoints as a dict with the db_name as the key
def lambda_handler(event, context):

    db_instances = describe_db_instances("ap-southeast-2")
    return_object = {}
    return_everything = True

    # the list of db names was requested, put those in the return object
    if 'name_list' in event:
        return_everything = False
        return_object['name_list'] = []
    # loop over the instances, pull out the name Tag
        for DBInstance in db_instances['DBInstances']:
            for Tag in DBInstance['TagList']:
                if Tag['Key'] == 'Name':
                    return_object['name_list'].append(Tag['Value'])
    
    if 'debug' in event:
        print('Generated name_list: ')
        print(json.dumps(return_object, default=str))

    # the list of endpoints was requested, put those in the return objects
    if 'list_endpoints' in event:
        return_everything = False
        return_object['db_endpoints'] = {}
        for DBInstance in db_instances['DBInstances']:
            for Tag in DBInstance['TagList']:
                if Tag['Key'] == 'Name':
                    return_object['db_endpoints'][Tag['Value']] =  DBInstance['Endpoint']

    if return_everything:
        return {
            'statusCode': 200,
            'body': json.dumps(db_instances, default=str)
        }
    else:
        return{
            'statusCode': 200,
            'body': return_object
        }
