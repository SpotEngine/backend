from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from utils.base_models import BaseModel
from utils.choices import AccountTypeChoice


class APIKey(BaseModel):
    account = models.ForeignKey("Account", on_delete=models.PROTECT)
    key = models.CharField(max_length=40, choices=AccountTypeChoice.choices, default=AccountTypeChoice.SUB)
