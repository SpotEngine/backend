from django.contrib import admin
from ..models import Setup
from utils.base_admin import BaseAdmin

@admin.register(Setup)
class SetupAdmin(BaseAdmin):
    list_display = ['id', 'account', 'margin', 'mode', 'leverage', 'contract',]
    list_filter = ['margin', 'mode', 'leverage', 'contract']