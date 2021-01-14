# noinspection PyUnresolvedReferences
import pyodbc
import re
import boto3
from enum import Enum

rds_client = boto3.client('rds')


class RdsServer:
    class DbFilter(Enum):
        PROD = 0x01
        TEST = 0x02
        HISTORIC = 0x04
        PG_SITE = 0x08
        MSSQL_SYSTEM = 0x20
        ALL = 0xFF

    def __init__(self, rds_data):

        self.db_instance_arn = rds_data['DBInstanceArn']
        self.db_instance_identifier = rds_data['DBInstanceIdentifier']
        self.address = rds_data['Endpoint']['Address']
        self.port = rds_data['Endpoint']['Port']
        self.odbc_connection = None

    def connect(self, credentials):
        try:
            self._odbc_connection = pyodbc.connect(self._connection_string(credentials))
            self._log.info(
                "PBR???",
                "Connected to sqlServer='{server}' as user='{user}'",
                {'server': self.address, 'user': credentials.user}
            )

        except Exception as ex:
            self._log().warn(
                "PBR???",
                "Failed to connect to sqlServer='{server}' with error='{error}'",
                {'server': self.address, 'error': str(ex)}
            )
            raise ex

    def close(self):
        self._odbc_connection.close()

    def query(self, statement):
        cursor = self.odbc_connection.cursor()
        cursor.execute(statement)

        row = cursor.fetchone()
        while row:
            yield row
            row = cursor.fetchone()

    def execute(self, statement):
        cursor = self.odbc_connection.cursor()
        cursor.execute(statement)

    def _connection_string(self, credentials):
        connection_string_template = \
            "Driver={{ODBC Driver 17 for SQL Server}};Server={host};Integrated Security=false;" +\
            "uid={username};pwd={password};autocommit=True;"
        connection_string = connection_string_template.format(
            host=self.address,
            username=credentials.user,
            password=credentials.password
        )
        return connection_string

    @classmethod
    def find_instances(cls):
        try:
            for rds in rds_client.describe_db_instances()['DBInstances']:
                server = RdsServer(rds)
                cls.__log.info(
                    "PBR???",
                    "Found a rds instance with id='{id}' and address='{address}'",
                    {'address': server.address, 'id': server.db_instance_identifier}
                )

                yield server
        except Exception as ex:
            cls.__log.warn(
                "PBR???",
                "rds_client.describe_db_instances() threw an exception='{ex}'",
                {'ex': str(ex)}
            )

    @classmethod
    def tag_filter(cls, tag_filter):
        def rds_tag_filter_impl(rds):
            cls.__log.info(
                "PBR???",
                "Looking for tags on RDS instance='{i}'.",
                {'i': str(rds)}
            )
            tags = rds_client.list_tags_for_resource(ResourceName=rds.db_instance_arn)['TagList']

            for f in tag_filter:
                if len(list(filter(lambda x: x['Key'] == f['Key'] and x['Value'] == f['Value'], tags))) == 0:
                    cls.__log.info(
                        "PBR???",
                        "tag_filter is rejecting server='{s}' because it did not have a tag='{t}' with the " +
                        "value='{v}'.",
                        {'s': rds.db_instance_identifier, 't': f['Key'], 'v': f['Value']}
                    )
                    return False
            cls.__log.info(
                "PBR???",
                "The RDS server='{s}' is selected by the tag_filter.", {'s': rds.db_instance_identifier}
            )
            return True

        return rds_tag_filter_impl

    @classmethod
    def db_regex_list(cls):
        return {
            RdsServer.DbFilter.PROD: re.compile("^PG[0-9]{4}[A-Z]{2}$"),
            RdsServer.DbFilter.TEST: re.compile("^PG[0-9]{4}[A-Z]{2}_Test.*$"),
            RdsServer.DbFilter.HISTORIC: re.compile("^PG[0-9]{4}[A-Z]{2}_Historic.*$"),
            RdsServer.DbFilter.PG_SITE: re.compile("^PG[0-9]{4}[A-Z]{2}.*$"),
            RdsServer.DbFilter.ALL: re.compile("^.+$"),
            RdsServer.DbFilter.MSSQL_SYSTEM: re.compile("^(?!PG[0-9]{4}).*$")  # Does not start with PGnnnn
        }

    @classmethod
    def db_filter(cls, db_flags):
        filter_regex_list = cls.db_regex_list()

        def db_filter_impl(db_data):
            db_name = db_data['db']
            for f in db_flags:
                if filter_regex_list[f].match(db_name):
                    cls.__log.trace(
                        "PBR???",
                        "db_filter has decided that db_name='{db_name}' matches the regex='{f}'",
                        {'db_name': db_name, 'f': str(f)}
                    )
                    return True

            cls.__log.trace(
                "PBR???",
                "db_filter has decided that db_name='{db_name}' did not match any regex expressions",
                {'db_name': db_name}
            )
            return False

        return db_filter_impl

    @property
    def db_instance_arn(self):
        return self.__db_instance_arn

    @db_instance_arn.setter
    def db_instance_arn(self, value):
        self.__db_instance_arn = value

    @property
    def db_instance_identifier(self):
        return self.__db_instance_identifier

    @db_instance_identifier.setter
    def db_instance_identifier(self, value):
        self.__db_instance_identifier = value

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, new_value):
        self.__address = new_value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, new_value):
        self.__port = new_value

    @property
    def odbc_connection(self):
        return self._odbc_connection

    @odbc_connection.setter
    def odbc_connection(self, new_value):
        self._odbc_connection = new_value

    #
    #  Add Logging Context support for this class
    #
    from rdsbackup.Log import Log, LogLevel
    __log = Log(__file__, LogLevel.TRACE)

    @property
    def _log(self):
        return self.__log

    @_log.setter
    def _log(self, value):
        self.__log = value
