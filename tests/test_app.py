import pytest

from pytest_chalice.handlers import RequestHandler

from http import HTTPStatus
import base64
import os
import hmac
import hashlib
import json


class TestCallback:
    @pytest.fixture
    def url(self) -> str:
        return '/callback'

    def test_post_200(self, url: str, client: RequestHandler) -> None:
        request_json = json.dumps({
            'events': [{
                'type': 'message',
                'replyToken': '7c8a3dcb6eb94eb790a2d3bb38f12f93',
                'source': {
                    'userId': '',
                    'type': 'user'
                },
                'timestamp': 1571754325743,
                'message': {
                    'type': 'text',
                    'id': '10786671259466',
                    'text': 'Hello'
                }
            }],
            'destination': ''
        })
        signature = base64.b64encode(hmac.new(
            os.environ['LINE_CHANNEL_SECRET'].encode('utf-8'),
            request_json.encode('utf-8'),
            hashlib.sha256,
        ).digest()).decode('utf-8')

        headers = {'X-Line-Signature': signature, 'Content-Type': 'application/json'}
        response = client.post(url, headers=headers, body=request_json)

        assert response.status_code == HTTPStatus.OK

    def test_post_400(self, url: str, client: RequestHandler) -> None:
        headers = {'X-Line-Signature': ''}
        response = client.post(url, headers=headers)
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(
        'method',
        ('get', 'head', 'put', 'delete', 'trace', 'patch', 'link', 'unlink'),
    )
    def test_405(self, method: str, url: str, client: RequestHandler) -> None:
        response = getattr(client, method)(url)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
