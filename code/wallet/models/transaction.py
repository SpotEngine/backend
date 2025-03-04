from django.db import models
from utils.choices import TranactionTypeChoice, TranactionStatusChoice

from utils.base_models import BaseModel, base_decimal
from django.contrib.auth.models import User


class Transaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    token = models.ForeignKey('Token', on_delete=models.CASCADE, null=True, blank=True)
    amount = base_decimal()
    tx_hash = models.CharField(max_length=80, null=True, blank=True, unique=True)
    type = models.CharField(max_length=20, choices=TranactionTypeChoice.choices, default=TranactionTypeChoice.DEPOSIT)
    status = models.CharField(max_length=20, choices=TranactionStatusChoice.choices, default=TranactionStatusChoice.PENDING)


    @classmethod
    def create_deposit(cls, user, token, tx_hash,):
        deposit = cls(
            user=user,
            token=token,
            tx_hash=tx_hash,
            type=TranactionTypeChoice.DEPOSIT,
            status=TranactionStatusChoice.PENDING
        )
        deposit.save()
        return deposit

    @classmethod
    def create_withdraw(cls, user, token, amount,):
        withdraw = cls(
            user=user,
            token=token,
            amount=amount,
            type=TranactionTypeChoice.WITHDRAW,
            status=TranactionStatusChoice.PENDING
        )
        withdraw.save()
        return withdraw
    