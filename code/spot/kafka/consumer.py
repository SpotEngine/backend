from confluent_kafka import Consumer
from utils.enums import KafkaSpotQueue
from django.conf import settings


def kafka_concumer(callback: callable):
    config = settings.KAFKA_CONSUMER_CONFIG
    config['group.id'] = 'spot-match-engine'
    c = Consumer(config)
    topics = [KafkaSpotQueue.SPOT_MATCH_ENGINE]
    c.subscribe(topics)
    print(f"consumer subscribed: {topics}, {config}")

    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue
        msg_value = msg.value().decode('utf-8')
        # print(msg_value)
        callback(msg_value)
