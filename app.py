from chalice import BadRequestError, Chalice
from chalice.app import SQSEvent

from linebot.models import MessageEvent, ImageMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError, LineBotApiError

import json

from chalicelib import sqs_queue_name, rekognition_client
from chalicelib.linebot_utils import download_and_resize_image, handler, line_bot_api


app = Chalice(app_name='LINEBotWorkshop')

CONFIDENCE_THRESHOLD = 70
PIXEL_RESIZE_TO = 256


@app.route('/callback', methods=['POST'])
def callback():
    signature = app.current_request.headers['X-Line-Signature']
    body = app.current_request.raw_body.decode('utf-8')

    try:
        handler.handle(body, signature)
    except InvalidSignatureError as e:
        raise BadRequestError(e)

    return 'OK'


@app.on_sqs_message(queue=sqs_queue_name, batch_size=1)
def handle_sqs_message(event: SQSEvent) -> None:
    for record in event:
        message_event: MessageEvent = MessageEvent.new_from_json_dict(json.loads(record.body))
        if not isinstance(message_event.message, ImageMessage):
            continue

        image: bytes = download_and_resize_image(message_event, PIXEL_RESIZE_TO)
        response = rekognition_client.detect_labels(Image={'Bytes': image})
        labels_to_reply = [l['Name'] for l in response['Labels'] if l['Confidence'] > CONFIDENCE_THRESHOLD]
        reply_message = ', '.join(labels_to_reply) if labels_to_reply else 'No label is detected, try another one'

        try:
            line_bot_api.reply_message(message_event.reply_token, TextSendMessage(text=reply_message))
        except LineBotApiError as e:
            if e.message == 'Invalid reply token':
                app.log.error(f'Failed to reply message: {message_event}')
            else:
                raise
