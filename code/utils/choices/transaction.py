from django.db import models
from django.utils.translation import gettext_lazy as _


class TranactionTypeChoice(models.TextChoices):
    DEPOSIT = 'deposit', _('deposit')
    WITHDRAW = 'withdraw', _('withdraw')


class TranactionStatusChoice(models.TextChoices):
    PENDING = 'pending', _('pending')
    ONCHAIN = 'onchain', _('onchain')
    DONE = 'done', _('done')
    FAILED = 'failed', _('failed')
