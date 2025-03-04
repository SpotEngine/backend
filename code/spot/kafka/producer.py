from confluent_kafka import Producer
from django.conf import settings

config = settings.KAFKA_PRODUCER_CONFIG
KafkaProducer = Producer(config)
print("KafkaProducer", config)
