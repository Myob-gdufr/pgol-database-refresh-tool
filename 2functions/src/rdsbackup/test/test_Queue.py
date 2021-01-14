import unittest
from rdsbackup.Queue import Queue

class TestQueue(unittest.TestCase):
    #
    #   Test Plan - receiving messages
    #
    #   1.  No incomming messages
    #
    #       Results in:
    #       -  a log entry confirming zero queue messages.
    #       -  a zero length result iterator.
    #       -  no exceptions being thrown externally.
    def test_no_incomming_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - receiving messages
    #
    #   2.  Receiving 1 message
    #
    #       Results in:
    #       -
    #       -  a result iterator with 1 item
    #       -  no exceptions being thrown externally.
    def test_one_incomming_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - receiving messages
    #
    #   3.  Receiving 10 messages.
    #
    #       Results in:
    #       -
    #       -  a result iterator with 10 items
    #       -  no exceptions being thrown externally.
    def test_10_incomming_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - receiving messages
    #
    #   4.  AWS authentication failure
    #
    #       Results in:
    #       -  an exception of botocore.exceptions.ClientError
    def test_authentication_failure_on_incomming_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - receiving messages
    #
    #   5.  AWS response not consistent with spec.
    #
    #       Results in:
    #       -
    #       -
    def test_invalid_response_on_incomming_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - receiving messages
    #
    #   6.  network failure
    #
    #       Results in:
    #       -
    #       -
    def test_network_timeout_on_incomming_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - receiving messages
    #
    #   7.  sqs arn does not exist
    #
    #       Results in:
    #       -
    #       -
    def test_invalid_arn_on_incomming_messages(self):
        self.assertTrue(False)


    #
    #   Test Plan - deleting messages
    #
    #   1.  valid ack_id, message still exists
    #
    #       Results in:
    #       -
    #       -
    def valid_ack_id_on_deleting_messages(self):
        url=""

        inputs={
            'ack_id': "",
            'boto_client':  None
        }

        expected= {}
        try:
            queue = Queue(url)
            results = queue.ack(**inputs)
        except Exception as ex:
            self.assertTrue(False, "No exceptions generated")

        #  Verify
        self.assertEqual(expected, results)

    #
    #   Test Plan - deleting messages
    #
    #   2.  valid ack_id, deleted by other valid ack_id.
    #
    #       Results in:
    #       -
    #       -
    def valid_ack_id_but_already_deleted_on_deleting_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - deleting messages
    #
    #   3.  expired ack_id, initially valid format, but message expired.
    #
    #       Results in:
    #       -
    #       -
    def expired_ack_id_on_deleting_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - deleting messages
    #
    #   4.  AWS authentication failure
    #
    #       Results in:
    #       -  an exception of botocore.exceptions.ClientError
    def authentication_failed_on_deleting_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - deleting messages
    #
    #   5.  AWS response not consistent with spec.
    #
    #       Results in:
    #       -
    #       -
    def invalid_response_on_deleting_messages(self):
        self.assertTrue(False)

    #
    #   Test Plan - deleting messages
    #
    #   6.  network failure
    #
    #       Results in:
    #       -
    #       -
    def network_failure_on_deleting_messages(self):
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
