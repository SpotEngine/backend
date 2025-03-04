from django.contrib import admin
from ..models import Position
from utils.base_admin import BaseAdmin


@admin.register(Position)
class PositionAdmin(BaseAdmin):
    list_display = ['id', 'account', 'contract', 'status', 'size', 'direction', 'margin', 'mode', 'leverage', 'margin_amount', 'entry_price', 'liquidation_price', "pnl"]
    list_filter = ['direction', 'margin', 'mode', 'status', 'contract', ]