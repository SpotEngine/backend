from django.contrib import admin
from ..models import Symbol
from utils.base_admin import BaseAdmin

@admin.register(Symbol)
class SymbolAdmin(BaseAdmin):
    list_display = ['symbol', 'base', 'quote', 'priority', 'is_active']
    list_filter = ['is_active']