from django.db import models
from django.utils.translation import gettext_lazy as _



class OrderStatusChoice(models.TextChoices):
    RECEIVED = 'received', _('received')
    PLACED = 'placed', _('placed')
    CANCELED = 'canceled', _('canceled')
    FILLED = 'filled', _('filled')

class OrderTimeInForceChoice(models.TextChoices):
    GTC = 'gtc', _('gtc')
    IOK = 'iok', _('iok')

