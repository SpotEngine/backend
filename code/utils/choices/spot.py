from django.db import models
from django.utils.translation import gettext_lazy as _


class SpotOrderTypeChoice(models.TextChoices):
    LIMIT = 'limit', _('limit')
    MARKET = 'market', _('market')
    # STOP_LIMIT = 'stop_limit', _('stop_limit')
    # STOP_MARKET = 'stop_market', _('stop_market')

class SpotOrderSideChoice(models.TextChoices):
    BUY = 'buy', _('buy')
    SELL = 'sell', _('sell')
