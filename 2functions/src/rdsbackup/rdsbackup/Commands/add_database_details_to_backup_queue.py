from rdsbackup.Credentials import Credentials
from rdsbackup.RdsServer import RdsServer
from rdsbackup.Queue import Queue
from rdsbackup.Utils import flatten, foreach
from rdsbackup.Log import Log, LogLevel
import json

#
#  Add Logging Context support for this file
#

__log = Log(__file__, LogLevel.TRACE)


def get_databases_on_server(credential_creator=Credentials.generate):
    __log.info("PBR???", "getting get_databases_on_server_impl.", {})

    def get_databases_on_server_impl(server):
        __log.info("PBR???", "we have get_databases_on_server.", {})

        try:
            credentials = credential_creator("BackupOperator", server)
            server.connect(credentials)
            for db_row in server.query("SELECT name FROM master.sys.databases"):
                __log.info("PBR???", "Found database='{db}' on sqlServer='{s}'.", {'db': str(db_row[0]), 's': server.db_instance_identifier})
                yield {
                    'db': str(db_row[0]),
                    'server': server.db_instance_identifier
                }

            server.close()

        # If we have an exception in processing this server, we still want to continue
        # and process the next server
        except Exception as ex:
            __log.warn("PBR???", "getting databases from the rds server='{s}' failed with the message='{ex}'.",
                     {'s': server.db_instance_identifier, 'ex': str(ex)})

    return get_databases_on_server_impl


def send_database_to_sqs_queue(sqs_tags):
    queues = list(filter(Queue.tag_filter(sqs_tags), Queue.find_instances(prefix="QueueDBForNightlyBackup")))

    def send_database_to_sqs_queue_impl(db_data):
        print("making data label")
        data_label = "{s}:{db}".format(**{'s': db_data['server'], 'db': db_data['db']})
        print("made data label: " + data_label)

        serialized_data = json.dumps(db_data)
        __log.info("PBR???", "Preparing to send database='{db}' on sqlServer='{s}' with label='{l}' to queues='{q}'.",
                 {'db': db_data['db'], 's': db_data['server'], 'q': len(queues), 'l': data_label})
        for q in queues:
            try:
                q.send(serialized_data, data_label, message_group=db_data['server'])
            except Exception as ex:
                __log.warn(
                    "PBR???",
                    "sending database='{db}' from the rds server='{s}' to the queue='{q}' failed with the "
                    "message='{ex}'.",
                    { 'db': db_data['db'], 's': db_data['server'], 'q':  q.url, 'ex': ex }
                )

    return send_database_to_sqs_queue_impl


def add_database_details_to_backup_queue_impl(vpc_name, db_filter_enums=[RdsServer.DbFilter.ALL]):
    try:
        __log.notice("PBR???",
                     "Processing RDS Instances in the vpc='{vpc}' for databases that match the filters='{filters}'",
                     {'vpc': vpc_name, 'filters': str(db_filter_enums)})
        # lets get our closures ready.
        #  Define which RDS instances are selected, based on tag values
        tag_filter = RdsServer.tag_filter([
            {'Key': 'VPC', 'Value': vpc_name},
            {'Key': 'Role', 'Value': 'CustomerData'}
        ])

        #  Define which databases are selected, based on DB name matching pre-canned regular expressions.
        db_filter = RdsServer.db_filter(db_filter_enums)

        queue_db = send_database_to_sqs_queue([
            {'VPC': vpc_name},
            {'Role': 'QueueDBForNightlyBackup'}
        ])

        #  Now we connect up the work flow:
        databases = list(
            flatten(foreach(queue_db,
            filter(db_filter,
            flatten(map(get_databases_on_server(),
            flatten(filter(tag_filter, RdsServer.find_instances())
        )))))))

        # print(str(databases))

    except Exception as ex:
        __log.error("PBR???", "The command='Add databases to backup queue' failed with an unhandled exception='{ex}'",
                    {'ex': str(ex)})


def script():
    import argparse

    parser = argparse.ArgumentParser(description='Add the list of databases to the database backup queue')
    parser.add_argument('--vpc-name', dest='vpc_name',
                        help='The name of the VPC to backup')

    args = parser.parse_args()
    add_database_details_to_backup_queue_impl(args.vpc_name)


if __name__ == '__main__':
    script()
