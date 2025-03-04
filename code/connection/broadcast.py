from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Broadcast:
    channel_layer = get_channel_layer()

    @classmethod
    def batch_publish(cls, updates):
        for update in updates:
            cls.publish(**update)

    @classmethod
    def publish(cls, channel, message):
        async_to_sync(cls.channel_layer.group_send)(channel, {
            "type": "chat.message",
            "message": message,
        })