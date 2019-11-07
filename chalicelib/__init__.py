import boto3

import os


sqs = boto3.resource('sqs')
sqs_queue_name = os.environ['SQS_QUEUE_NAME']

rekognition_client = boto3.client('rekognition')


class __ObjectManager:
    _sqs_queue = None

    @property
    def sqs_queue(self) -> 'boto3.resources.factory.sqs.Queue':
        if not self._sqs_queue:
            self._sqs_queue = sqs.get_queue_by_name(QueueName=sqs_queue_name)
        return self._sqs_queue


__om = __ObjectManager()


def get_sqs_queue() -> 'boto3.resources.factory.sqs.Queue':
    return __om.sqs_queue
