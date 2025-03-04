from django.db import models
from django.utils.translation import gettext_lazy as _



class PerpOrderTypeChoice(models.TextChoices):
    LIMIT = 'limit', _('limit')
    MARKET = 'market', _('market')
    # STOP_LIMIT = 'stop_limit', _('stop_limit')
    # STOP_MARKET = 'stop_market', _('stop_market')

class PerpDirectionChoice(models.TextChoices):
    LONG = 'long', _('long')
    SHORT = 'short', _('short')


class PositionStatusChoice(models.TextChoices):
    OPEN = 'open', _('open')
    CLOSED = 'closed', _('closed')
    LIQUDATION = 'liquidation', _('liquidation')

class MarginModeChoice(models.TextChoices):
    # CROSS = 'cross', _('cross')
    ISOLATED = 'isolated', _('isolated')

class PositionModeChoice(models.TextChoices):
    # HEDGE = 'hedge', _('hedge')
    ONEWAY = 'oneway', _('oneway')

