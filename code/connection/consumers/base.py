import json

from channels.generic.websocket import AsyncWebsocketConsumer


class BaseConsumer(AsyncWebsocketConsumer):
    class Meta:
        abstract = True

    async def connect(self):
        self.subscribed_channels = set()
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        channels = data.get('channels', [])
        if action == 'subscribe':
            for channel in channels:
                await self.subscribe(channel=channel)
        elif action == 'unsubscribe':
            for channel in channels:
                await self.unsubscribe(channel=channel)
        await self.send(text_data=json.dumps({"subscribed_channels": list(self.subscribed_channels)}))


    async def subscribe(self, channel):
        await self.channel_layer.group_add(channel, self.channel_name)
        self.subscribed_channels.add(channel)

    async def unsubscribe(self, channel):
        await self.channel_layer.group_discard(channel, self.channel_name)
        self.subscribed_channels.remove(channel)

    async def disconnect(self, close_code):
        for channel in self.subscribed_channels:
            await self.channel_layer.group_discard(channel, self.channel_name)
        await super().disconnect(close_code)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))