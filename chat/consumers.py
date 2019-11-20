from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
class ChatConsumer(AsyncWebsocketConsumer):
    async def fetch_messages(self, data):
        print("fetching...")
        pass
    async def new_message(self, data):
        print("new message")

        pass

    command = {
        'fetch messages' : fetch_messages,
        'new_message' : new_message,
    }
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        self.command[data[command]](self, data)

    async def send_chat_message(self, message):   
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
