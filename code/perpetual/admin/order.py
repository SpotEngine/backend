from django.contrib import admin
from ..models import Order
from utils.base_admin import BaseAdmin

@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ['id', 'account', 'type', 'contract', 'direction', 'price', 'size', 'filled_size', 'quote_quantity', 'filled_quote_quantity', 'status', 'locked',]
    list_filter = ['type', 'status', 'direction', 'contract', ]