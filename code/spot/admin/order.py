from django.contrib import admin
from ..models import Order
from utils.base_admin import BaseAdmin

@admin.register(Order)
class OrderAdmin(BaseAdmin):
    list_display = ['id', 'account', 'symbol', 'type', 'side', 'status', 'price', 'quantity', 'filled_quantity', 'locked_asset', 'locked_amount', 'fee_rebate']
    list_filter = ['side', 'type', 'status', 'symbol', 'locked_asset__token']