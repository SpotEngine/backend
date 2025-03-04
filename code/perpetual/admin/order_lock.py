from django.contrib import admin
from ..models import OrderLock
from utils.base_admin import BaseAdmin


@admin.register(OrderLock)
class OrderLockAdmin(BaseAdmin):
    list_display = ['id', 'account', 'asset' ,'amount' ,'position' ,'size' ,'fee']
    list_filter = ['asset__token']
