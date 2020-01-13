from typing import Iterable

import pytest

from aws_xray_sdk import global_sdk_config
from botocore.stub import Stubber
from chalice import Chalice

from linebot.models import MessageEvent

import os
import uuid

from app import app as chalice_app
from chalicelib import sqs

REGION = os.environ['AWS_DEFAULT_REGION']
ACCOUNT_ID = '123456789012'


@pytest.fixture(autouse=True)
def disable_xray() -> None:
    global_sdk_config.set_sdk_enabled(False)


@pytest.fixture
def app() -> Chalice:
    return chalice_app


@pytest.fixture(autouse=True)
def stub_sqs() -> Iterable[Stubber]:
    with Stubber(sqs.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()


@pytest.fixture
def stub_sqs_get_queue_url(stub_sqs: Stubber) -> None:
    queue_name = os.environ['SQS_QUEUE_NAME']
    stub_sqs.add_response(
        'get_queue_url',
        expected_params={'QueueName': queue_name},
        service_response={'QueueUrl': f'https://{REGION}.queue.amazonaws.com/{ACCOUNT_ID}/{queue_name}'}
    )


@pytest.fixture
def stub_sqs_send_message(stub_sqs: Stubber) -> None:
    stub_sqs.add_response(
        'send_message',
        service_response={'MD5OfMessageBody': '', 'MessageId': str(uuid.uuid4())}
    )


@pytest.fixture
def fx_message_event() -> MessageEvent:
    return MessageEvent.new_from_json_dict({
        'message': {
            'contentProvider': {
                'type': 'line',
            },
            'id': '10780982258255',
            'type': 'image',
        },
        'replyToken': '776377ba91dc4d72bbf0ded24edb0dbd',
        'source': {
            'type': 'user',
            'userId': '',
        },
        'timestamp': 1571669106624,
        'type': 'message',
    })
