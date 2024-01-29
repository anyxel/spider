import os
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def is_file_exists(filepath):
    if os.path.isfile(filepath):
        return True
    else:
        return False


def send_message_to_websocket(message):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "terminal",
        {
            "type": "chat.message",
            "message": message,
        },
    )


async def send_message_to_websocket_async(message):
    channel_layer = get_channel_layer()

    await channel_layer.group_send("terminal", {
        "type": "chat.message",
        "message": message,
    })
