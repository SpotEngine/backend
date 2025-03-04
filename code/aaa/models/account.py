from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from utils.base_models import BaseModel
from utils.choices import AccountTypeChoice
from django.contrib.auth.models import User

class Account(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=AccountTypeChoice.choices, default=AccountTypeChoice.MAIN)

    def __str__(self):
        return f"{self.id}"

    @classmethod
    def create(cls, user, type=AccountTypeChoice.SUB):
        account = cls(user=user, type=type)
        account.save()
        return account
