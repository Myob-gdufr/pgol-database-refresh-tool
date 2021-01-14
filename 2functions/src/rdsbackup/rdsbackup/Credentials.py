import json
from rdsbackup import Log
import boto3

sm_client = boto3.client('secretsmanager')


class Credentials:
    def __init__(self, secret_value):
        data = json.loads(secret_value)
        self.user = data['username']
        self.password = data['password']

    @property
    def user(self):
        return self.__user

    @user.setter
    def user(self, new_value):
        self.__user = new_value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_value):
        self.__password = new_value

    @classmethod
    def generate(cls, role, rds_server, aws_client=sm_client):
        try:
            secret_name = role + "-" + rds_server.db_instance_identifier
            get_secret_value_response = aws_client.get_secret_value(SecretId=secret_name)
            credentials = Credentials(get_secret_value_response['SecretString'])
            return credentials
        except Exception as ex:
            cls.__log.warn(
                "PBR???",
                "generating credentials for the role='{r}' on the rds server='{s}' failed with the message='{ex}'.",
                {'r': role, 's': rds_server.db_instance_identifier, 'ex': str(ex)}
            )
            raise ex

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
