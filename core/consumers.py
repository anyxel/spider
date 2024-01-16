import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('conn')
        self.group_name = "terminal"  # Set the group name
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('rcv')
        data = json.loads(text_data)
        message = data['message']

        # Perform some action with the received message
        await self.send(text_data=json.dumps({
            'message': f"You said: {message}"
        }))

    async def chat_message(self, event):
        # print('event')
        # Send the message to the WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
