import io
import os
from PIL import Image, ImageFile

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, ImageMessage
from linebot.models.responses import Content

from . import get_sqs_queue


ImageFile.LOAD_TRUNCATED_IMAGES = True

channel_secret = os.environ['LINE_CHANNEL_SECRET']
channel_access_token = os.environ['LINE_CHANNEL_ACCESS_TOKEN']

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event: MessageEvent) -> None:
    queue = get_sqs_queue()
    queue.send_message(MessageBody=str(event))


def download_and_resize_image(message_event: MessageEvent, pixel_resize_to: int) -> bytes:
    src_image = io.BytesIO()
    message_content: Content = line_bot_api.get_message_content(message_event.message.id)

    for chunk in message_content.iter_content():
        src_image.write(chunk)

    with Image.open(src_image) as img:
        width, height = img.size
        if width < pixel_resize_to and height < pixel_resize_to:
            return src_image.getvalue()

        dst_image = io.BytesIO()
        img.thumbnail((pixel_resize_to, pixel_resize_to))
        img.save(dst_image, format=img.format)

    return dst_image.getvalue()
