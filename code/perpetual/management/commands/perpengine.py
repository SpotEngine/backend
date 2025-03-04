from django.core.management.base import BaseCommand, CommandError
from ...kafka.consumer import kafka_concumer 
from ...logics import receive_send_order_event, receive_cancel_order_event
from utils.enums import KafkaPerpEvent
import json
import time



class Command(BaseCommand):
    help = "Starting Perpetual match engine"

    def handle(self, *args, **options):
        def event_handler(event):
            t1 = time.time()
            event = json.loads(event)
            if event['topic'] == KafkaPerpEvent.SEND_ORDER:
                receive_send_order_event(event['event'])
            elif event['topic'] == KafkaPerpEvent.CANCEL_ORDER:
                receive_cancel_order_event(event['event'])
            t2 = time.time()
            print(f"done in {t2 - t1} s")

        kafka_concumer(event_handler)




