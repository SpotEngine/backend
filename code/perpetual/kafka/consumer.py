from confluent_kafka import Consumer
from utils.enums import KafkaPerpQueue
from django.conf import settings


def kafka_concumer(callback: callable):
    c = Consumer({
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'match-engine',
        'auto.offset.reset': 'earliest',
    })
    topics = [KafkaPerpQueue.PERP_MATCH_ENGINE]
    c.subscribe(topics)
    print(f"consumer subscribed: {topics}")

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        msg = msg.value().decode('utf-8')
        # print(msg)
        callback(msg)
