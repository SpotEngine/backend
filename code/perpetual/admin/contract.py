from django.contrib import admin
from ..models import Contract
from utils.base_admin import BaseAdmin

@admin.register(Contract)
class ContractAdmin(BaseAdmin):
    list_display = ['symbol', 'lot_size', 'margin', 'margin_amount', 'priority',]