from django.contrib import admin
from ..models import Trade
from utils.base_admin import BaseAdmin


@admin.register(Trade)
class TradeAdmin(BaseAdmin):
    list_display = ['id', 'order', 'match_tag', 'contract', 'price', 'size', 'is_maker', 'paid_token', 'paid_amount', 'paid_fee', 'received_amount', 'received_rebate']
    list_filter = ['is_maker', 'contract',]
