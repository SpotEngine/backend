from .producer import KafkaProducer
# from internal import enums
import time
import json
from utils.enums import KafkaPerpEvent, KafkaPerpQueue


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


def publish(info, event_type: KafkaPerpEvent,):
    events = []
    info['timestamp'] = int(1000 * time.time())
    if event_type == KafkaPerpEvent.SEND_ORDER:
        events.append({
            "info": info,
            "queue": KafkaPerpQueue.PERP_MATCH_ENGINE,
            "topic": KafkaPerpEvent.SEND_ORDER,
            "key": info['contract'],
        })
    elif event_type == KafkaPerpEvent.CANCEL_ORDER:
        events.append({
            "info": info,
            "queue": KafkaPerpQueue.PERP_MATCH_ENGINE,
            "topic": KafkaPerpEvent.CANCEL_ORDER,
            "key": info['contract'],
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