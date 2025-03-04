from decimal import Decimal

ZERO = Decimal('0.0')

class BaseUrl:
    MARKET = 'market/'
    TRADER = 'trader/'
    STAFF = 'staff/'

class OrderType:
    LIMIT = 'limit'
    MARKET = 'market'

class KafkaSpotQueue:
    SPOT_MATCH_ENGINE = 'spotMatchEngine'

class KafkaSpotEvent:
    SEND_ORDER = 'SEND_ORDER'
    CANCEL_ORDER = 'CANCEL_ORDER'

class KafkaPerpQueue:
    PERP_MATCH_ENGINE = 'perpetualMatchEngine'

class KafkaPerpEvent:
    SEND_ORDER = 'SEND_ORDER'
    CANCEL_ORDER = 'CANCEL_ORDER'


class SystemGeneratedEvent:
    LIQUIDATION_ORDER = "LIQUIDATION_ORDER"
