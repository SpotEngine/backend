from typing import Iterable
from django.db import models
from decimal import Decimal
from django.core import validators
from django.conf import settings
from utils.enums import ZERO


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']

    @property
    def ctime(self):
        return int(self.created_at.timestamp() * 1000)

    @property
    def utime(self):
        return int(self.updated_at.timestamp() * 1000)

    def save(self, *args, **kwargs) -> None:
        for key, value in self.__dict__.items():
            if isinstance(value, Decimal):
                self.__setattr__(key, value.normalize())
        self.full_clean()
        return super().save(*args, **kwargs)

def base_decimal(default=ZERO, max_digits=settings.BASE_MODEL_MAX_DIGITS, decimal_places=settings.BASE_MODEL_DECIMAL_PLACES, non_negative=True, **kwargs):
    if non_negative:
        validators_list = kwargs.get('validators', [])
        validators_list.append(
            validators.MinValueValidator(ZERO),
        )
        kwargs['validators'] = validators_list
    return models.DecimalField(
        default=default, 
        max_digits=max_digits, 
        decimal_places=decimal_places, 
        null=True, blank=True,  
        **kwargs
        )