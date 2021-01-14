from rdsbackup.Credentials import Credentials
from rdsbackup.Queue import Queue
from rdsbackup.RdsServer import RdsServer
from rdsbackup.Utils import merge_hash, foreach, multimap, flatten
import json
from functools import reduce
from rdsbackup.Log import Log, LogLevel
import uuid
from datetime import timezone, timedelta, datetime, date, time

#
#  Add Logging Context support for this file
#

__log = Log(__file__, LogLevel.TRACE)


def delete_message_from_queue():
    def delete_message_from_queue_impl(backup_message):
        try:
            __log.info(
                "PBR???",
                "The function backup_database_from_queue:delete_message_from_queue_impl() has been called"
                "with message='{m}'",
                {'m': str(backup_message)}
            )
            ack_token = backup_message['ack_token']
            message_id = backup_message['message_id']
            Queue(backup_message['queue_url']).ack(message_id, ack_token)
        except Exception as ex:
            __log.warn("PBR???", "When we attempted to delete the message='{m}', we received this exception='{ex}'",
                     {'ex': str(ex), 'm': str(backup_message)})
            raise ex

    return delete_message_from_queue_impl


def trigger_backup(vpc, s3_format, credential_creator=Credentials.generate):
    sql_template = \
        """
        exec msdb.dbo.rds_backup_database @source_db_name='{db}', @s3_arn_to_backup_to='{s3url}', @overwrite_S3_backup_file=1;
        commit;
        """

    def trigger_backup_impl(backup_message):
        try:
            __log.info(
                "PBR???",
                "The function backup_database_from_queue:trigger_backup_impl() has been called with message='{m}'",
                {'m': str(backup_message)}
            )
            server = backup_message['server_object']
            credentials = credential_creator("BackupOperator", server)
            db = backup_message['db']
            server.connect(credentials)
            dt = datetime.now(tz=timezone(timedelta(hours=12)))
            sql_params = {
                'db': db,
                'vpc': vpc.lower(),
                'server': server.db_instance_identifier,
                'day': dt.strftime(format="%y%m%d"),
                'time': dt.strftime(format="%H%M%S"),
                'guid': str(uuid.uuid4())
            }
            sql_cmd = sql_template.format(db=db, s3url=s3_format.format(** sql_params))
            try:
                for db_row in server.query(sql_cmd):
                    __log.debug("PBR???", "SQL OUTPUT: {sql}", {'sql': str(db_row)})
                yield backup_message

            except Exception as ex:
                __log.warn("PBR???", "SQL Execution Error exception='{ex}'",
                           {'ex': str(ex)})
                raise ex
            finally:
                server.close()

        except Exception as ex:
            __log.warn("PBR???", "When trying to trigger the backup, trigger_backup_impl caught this exception='{ex}'",
                       {'ex': ex}
                       )

    return trigger_backup_impl


def find_rds_instance(tag_filter_servers, server_list=RdsServer.find_instances()):
    #  Get the list of possible RDS servers.
    __log.info(
        "PBR???",
        "The function backup_database_from_queue:find_rds_instance() is about to build a list of servers.",
        {})
    servers = reduce(lambda mem, rds: merge_hash(mem, {rds.db_instance_identifier: rds}),
                     flatten(filter(tag_filter_servers, server_list)
                             ), {})
    __log.info("PBR???",
               "The function backup_database_from_queue:find_rds_instance() has built a list of count={c} servers.",
               {'c': len(servers.keys())}
               )

    def find_rds_instance_impl(backup_message):
        __log.info("PBR???", "The function backup_database_from_queue:find_rds_instance_impl() has been called with "
                             "message='{m}'",
                   {'m': str(backup_message)}
                   )
        try:
            if backup_message['server'] in servers:
                response = merge_hash({
                    'server_object': servers[backup_message['server']],
                }, backup_message)
                __log.info(
                    "PBR???",
                    "We are using server_object='{so}' to handle the SQL connection for database='{d}' on server'{s}'.",
                    {'so': response['server_object'], 's': response['server'], 'd': response['db']}
                )
                yield response
            else:
                __log.warn(
                    "PBR???",
                    "Then server='{s}' is not available, so we cannot backup its database='{d}'.",
                    {'s': backup_message['server'], 'd': backup_message['db']}
                )


        except Exception as ex:
            __log.warn("PBR???", "During attempting to backup, we encountered this exception='{ex}'", {'ex': ex})
            raise ex

    return find_rds_instance_impl


def read_database_from_sqs_queue(max_message_count=1):
    def read_database_from_sqs_queue_impl(queue):
        __log.warn("PBR???", "Called read_database_from_sqs_queue_impl", {})
        for m in queue.receive(max_message_count):
            body = json.loads(m['Body'])
            __log.info(
                "PBR???",
                "We have received a messageId='{m}' to backup database='{d}' on server='{s}'.",
                {'d': body['db'], 's': body['server'], 'm': m['MessageId']}
            )
            yield {
                'db': body['db'],
                'server': body['server'],
                'ack_token': m['ReceiptHandle'],
                'queue_url': m['QueueUrl'],
                'message_id': m['MessageId']
            }

    return read_database_from_sqs_queue_impl


def backup_database_from_queue_impl(vpc_name, s3_format="arn:aws:s3:::rds-{vpc}/Backup/{db}/{server}-{db}-{day}-{time}-{guid}"):
    sqs_queue_tags = [
        {'VPC': vpc_name},
        {'Role': 'QueueDBForNightlyBackup'}
    ]

    find_rds_server_for_backup = find_rds_instance(RdsServer.tag_filter([
        {'Key': 'VPC', 'Value': vpc_name},
        {'Key': 'Role', 'Value': 'CustomerData'}
    ]))

    #  Now we connect up the work flow:
    databases = list(
        map(delete_message_from_queue(),
        flatten(map(trigger_backup(vpc_name, s3_format),
        flatten(map(find_rds_server_for_backup,
        multimap(read_database_from_sqs_queue(),
        filter(Queue.tag_filter(sqs_queue_tags),
        Queue.find_instances(prefix="QueueDBForNightlyBackup"))
    )))))))

    print(str(databases))
    __log.info("PBR???", "backup_database_from_queue_impl has triggered the backup of count='{c}' databases",
               {'c': len(databases)})


def script():
    import argparse

    parser = argparse.ArgumentParser(description='Add the list of databases to the database backup queue')
    parser.add_argument('--vpc-name', nargs=1, dest='vpc_name', help='The name of the VPC to backup')
    parser.add_argument('--s3-format', nargs=1, dest='s3_format', help='a format string for the s3 backup file locations')

    args = parser.parse_args()
    backup_database_from_queue_impl(**vars(args))


if __name__ == '__main__':
    script()
