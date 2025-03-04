from django.core.management.base import BaseCommand, CommandError
from spot.kafka.consumer import kafka_concumer 
from spot.logics.match import receive_send_order_event, receive_cancel_order_event
from utils.enums import KafkaSpotEvent
import json
import time



class Command(BaseCommand):
    help = "Starting Spot match engine"

    def handle(self, *args, **options):
        def event_handler(event):
            t1 = time.time()
            event = json.loads(event)
            if event['topic'] == KafkaSpotEvent.SEND_ORDER:
                receive_send_order_event(event['event'])
            elif event['topic'] == KafkaSpotEvent.CANCEL_ORDER:
                receive_cancel_order_event(event['event'])
            t2 = time.time()
            print(f"done in {t2 - t1} s")

        kafka_concumer(event_handler)




