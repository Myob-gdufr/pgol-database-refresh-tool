import boto3
import uuid
from rdsbackup.Utils import merge_hash

sqs_client = boto3.client('sqs')


class Queue:
    def __init__(self, sqs_data):
        self.url = sqs_data

    def send(self, data, data_label, message_group=None, boto_client=sqs_client):
        try:
            message_params = {
                'QueueUrl': self.url,
                'MessageBody': data
            }
            if message_group is not None:
                message_params['MessageGroupId'] = message_group
                message_params['MessageDeduplicationId'] = str(uuid.uuid4())

            boto_client.send_message(**message_params)
            self._log.info("PBR???", "Sent data='{data}' to sqs queue='{q}'.", {'data': data_label, 'q': self.url})
        except Exception as ex:
            self._log.warn(
                "PBR???",
                "When attempting to send data='{data}' to sqs queue='{q}' we received the exception='{ex}'",
                {'data': data_label, 'q': self.url, 'ex': str(ex)}
            )

    def receive(self, max_message_count=1, boto_client=sqs_client):
        try:
            message_params = {
                'QueueUrl': self.url
            }
            response = boto_client.receive_message(**message_params)
            message_count = len(response['Messages']) if 'Messages' in response.keys() else 0
            self._log.info(
                "PBR???",
                "When attempting to receive from the sqs queue='{q}' we received the responseMetadata='{r}' with " +
                "count='{c}' messages.",
                {'q': self.url, 'r': response['ResponseMetadata'], 'c': message_count}
            )
            if message_count > 0:
                for m in response['Messages']:
                    self._log.info(
                        "PBR???",
                        "received messageId='{mid}' from the sqs queue='{q}' ",
                        {'q': self.url, 'mid': m['MessageId']}
                    )
                    yield merge_hash({'QueueUrl': self.url}, m)
        except Exception as ex:
            self._log.warn(
                "PBR???",
                "When attempting to receive from the sqs queue='{q}' we received the exception='{ex}'",
                {'q': self.url, 'ex': str(ex)}
            )
            raise ex

    def ack(self, message_id, ack_id, boto_client=sqs_client):
        try:
            boto_client.delete_message(QueueUrl=self.url, ReceiptHandle=ack_id)
            self._log.info(
                "PBR???",
                "Successfully deleted messageId='{mid}' from the sqs queue='{q}' ",
                {'mid': message_id, 'q': self.url}
            )

        except Exception as ex:
            self._log.warn(
                "PBR???",
                "When attempting to acknowledge from the sqs queue='{q}' we received the exception='{ex}'",
                {'q': self.url, 'ex': str(ex)}
            )
            raise ex

    @classmethod
    def find_instances(cls, prefix=''):
        response = sqs_client.list_queues(QueueNamePrefix=prefix)
        if 'QueueUrls' in response.keys():
            for sqs in response['QueueUrls']:
                queue = Queue(sqs)
                cls.__log.info(
                    "PBR???",
                    "Found SQS queue='{q}' with prefix='{p}' that may be a target for database names.",
                    {'q': queue.url, 'p': prefix}
                )
                yield queue
        else:
            cls.__log.warn(
                "PBR???",
                "There are no SQS Queues with the prefix='{p}'. No databases will be backed up.",
                {'p': prefix}
            )

    @classmethod
    def tag_filter(cls, tag_filter):
        def rds_tag_filter_impl(queue):
            tags = sqs_client.list_queue_tags(QueueUrl=queue.url)['Tags']
            for f in tag_filter:
                f_key = next(iter(f.keys()))
                f_value = next(iter(f.values()))
                cls.__log.trace(
                    "PBR???",
                    "tag_filter on queue='{q}' is comparing tag='{t}' with the value='{v}' in queue_tags='{qt}'.",
                    {'q': queue.url, 't': f_key, 'v': f_value, 'qt': list(tags.items())}
                )
                if len(list(filter(lambda x: (f_key == x[0]) and (f_value == x[1]), tags.items()))) == 0:
                    cls.__log.info(
                        "PBR???",
                        "tag_filter is rejecting queue='{q}' because it did not have a tag='{t}' with the value='{v}'.",
                        {'q': queue.url, 't': f_key, 'v': f_value})
                    return False
            cls.__log.info("PBR???", "The queue='{q}' is selected by the tag_filter.", {'q': queue.url})
            return True

        return rds_tag_filter_impl

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_value):
        self._url = new_value

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
