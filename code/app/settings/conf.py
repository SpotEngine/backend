import os
from decimal import Decimal

BASE_MODEL_MAX_DIGITS = 18
BASE_MODEL_DECIMAL_PLACES = 6
# REDIS_HOST = os.environ['REDIS_HOST']
# REDIS_PORT = os.environ['REDIS_PORT']
# REDIS_PASS = os.environ.get("REDIS_PASS")
# REDIS_USER = os.environ.get("REDIS_USER")
# REDIS_LOCATION = f'redis://{REDIS_USER}:{REDIS_PASS}@{REDIS_HOST}:{REDIS_PORT}'

# CACHES = {
#     "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": f"{REDIS_LOCATION}/0",
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient"
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['SERVICE_POSTGRES_DB'],
        'USER': os.environ['SERVICE_POSTGRES_USER'],
        'PASSWORD': os.environ['SERVICE_POSTGRES_PASSWORD'],
        'PORT': os.environ['POSTGRES_PORT'],
        'HOST': os.environ['POSTGRES_HOST'],
    }
}

# RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
# RABBITMQ_PORT = os.environ['RABBITMQ_PORT']

# RABBITMQ_USER = os.environ['RABBITMQ_USER']
# RABBITMQ_PASS = os.environ['RABBITMQ_PASS']

# CELERY_BROKER_URL = f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//'
# # CELERY_TASK_DEFAULT_QUEUE = 'accounting-internal'
# CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# CELERY_RESULT_SERIALIZER = 'json'
# CELERY_TASK_SERIALIZER = 'json'



ENVIRONMENT = os.environ['ENVIRONMENT']

# To support https in swagger:
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ['REDIS_HOST'], 6379)],
            # "hosts": [{
            # "address": f"rediss://{os.environ['REDIS_HOST']}:6379",  # "REDIS_TLS_URL"
            # "ssl_cert_reqs": None,
            # }]
        },
    },
}
_KAFKA_SERVERS = [
    {
        "host": os.environ['KAFKA_HOST1'],
        "port": os.getenv('KAFKA_HOST1PORT', '9092'),
    },
    # {
    #     "host": os.getenv('KAFKA_HOST2', ''),
    #     "port": os.getenv('KAFKA_HOST2PORT', '9092'),
    # },
    # {
    #     "host": os.getenv('KAFKA_HOST3', ''),
    #     "port": os.getenv('KAFKA_HOST3PORT', '9092'),
    # },
]
KAFKA_BOOTSTRAP_SERVERS = ','.join([
    f"{bootstrap_server['host']}:{bootstrap_server['port']}" for bootstrap_server in _KAFKA_SERVERS if bootstrap_server['host']]
)

KAFKA_API_KEY = os.environ['KAFKA_API_KEY']
KAFKA_API_SECRET = os.environ['KAFKA_API_SECRET']
KAFKA_BASE_CONF = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',  # or 'SCRAM-SHA-256' depending on your setup
    'sasl.username': KAFKA_API_KEY,
    'sasl.password': KAFKA_API_SECRET,
    # 'client.id': f'client-{os.uname().nodename}',  # Use hostname as client ID
}
KAFKA_CONSUMER_CONFIG = {
    **KAFKA_BASE_CONF, 
    # 'group.instance.id': f'instance-{os.uname().nodename}',  # Use hostname as client ID
    'auto.offset.reset': 'earliest',
    'session.timeout.ms': 6000,
    'heartbeat.interval.ms': 3000,    
}
KAFKA_PRODUCER_CONFIG = {
    **KAFKA_BASE_CONF, 
}
