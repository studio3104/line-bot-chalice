import pytest

from chalicelib.linebot_utils import handle_image_message, MessageEvent


@pytest.mark.usefixtures('stub_sqs_get_queue_url', 'stub_sqs_send_message')
def test_handle_image_message(fx_message_event: MessageEvent) -> None:
    handle_image_message(fx_message_event)
