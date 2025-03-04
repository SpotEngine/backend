from django.contrib import admin
from ..models import Asset
from utils.base_admin import BaseAdmin

@admin.register(Asset)
class AssetAdmin(BaseAdmin):
    list_display = ['id', 'account', 'token', 'free',]
    list_filter = ['token',]