from django.contrib import admin
from ..models import Token
from utils.base_admin import BaseAdmin

@admin.register(Token)
class TokenAdmin(BaseAdmin):
    list_display = ['ticker', 'name', 'is_transferable', 'account', 'supply', 'is_active']
    list_filter = ['is_transferable', 'is_active']