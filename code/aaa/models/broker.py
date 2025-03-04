from django.utils.translation import gettext_lazy as _
from django.db import models
from utils.base_models import BaseModel


class Broker(BaseModel):
    name = models.CharField(max_length=40, default="", null=True, blank=True)
    description = models.TextField(default="", null=True, blank=True)
