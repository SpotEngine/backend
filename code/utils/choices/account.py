from django.db import models
from django.utils.translation import gettext_lazy as _


class AccountTypeChoice(models.TextChoices):
    MAIN = 'main', _('main')
    SUB = 'sub', _('sub')
