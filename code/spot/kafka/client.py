from .producer import KafkaProducer
# from internal import enums
import time
import json
from utils.enums import KafkaSpotEvent, KafkaSpotQueue


def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
        success = False
    else:
        print('Message delivered to {} [{}]'.format(
            msg.topic(), msg.partition()))
        success = True
    return success


def publish(info, event_type: KafkaSpotEvent,):
    events = []
    info['timestamp'] = int(1000 * time.time())
    if event_type == KafkaSpotEvent.SEND_ORDER:
        events.append({
            "info": info,
            "queue": KafkaSpotQueue.SPOT_MATCH_ENGINE,
            "topic": KafkaSpotEvent.SEND_ORDER,
            "key": info['symbol'],
        })
    elif event_type == KafkaSpotEvent.CANCEL_ORDER:
        events.append({
            "info": info,
            "queue": KafkaSpotQueue.SPOT_MATCH_ENGINE,
            "topic": KafkaSpotEvent.CANCEL_ORDER,
            "key": info['symbol'],
        })


    for event in events:
        _produce(**event)


def _produce(info: dict, topic: str, key: str = "", queue: str = ""):
    event = {
        'topic': topic,
        'key': key,
        'timestamp': int(1000 * time.time()),
        'event': info,
    }
    # print(f"produce event: {event}")
    msg = json.dumps(event).encode('utf8')
    # if queue == enums.QueueName.match_engine.value:
    #     app.send_task("tasks.match_engine", args=[info], queue=queue)
    # else:
    #     event = {
    #         'topic': topic,
    #         'key': key,
    #         'timestamp': int(1000 * time.time()),
    #         'event': info,
    #     }
    #     app.send_task("tasks.publish_event", args=[event], queue=queue)
    KafkaProducer.produce(queue, key=key, value=msg, callback=delivery_report)