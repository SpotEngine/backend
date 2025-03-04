from django.db import models

from utils.base_models import BaseModel
from django.contrib.auth.models import User


class BlockchainWallet(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, unique=True)
    wallet_address = models.CharField(max_length=60, null=True, blank=True, unique=True)
