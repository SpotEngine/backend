from django.contrib import admin
from ..models import Trade
from utils.base_admin import BaseAdmin

@admin.register(Trade)
class TradeAdmin(BaseAdmin):
    list_display = ['id', 'match_tag', 'order', 'symbol', 'price', 'quantity', 'is_maker', 'paid_token', 'paid_amount', 'paid_rebate', 'received_token', 'received_amount', 'received_fee']
    list_filter = ['is_maker', 'symbol',]
