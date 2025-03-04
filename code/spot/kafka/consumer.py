from confluent_kafka import Consumer
from utils.enums import KafkaSpotQueue
from django.conf import settings


def kafka_concumer(callback: callable):
    config = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': 'spot-match-engine',
        'auto.offset.reset': 'earliest',
        'session.timeout.ms': 1000,
        'heartbeat.interval.ms': 3000,
        # 'group.instance.id': 'spot-match-engine-instance-1',  # should be unique for each instance
    }
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
