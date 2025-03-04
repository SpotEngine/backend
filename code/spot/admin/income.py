from django.contrib import admin
from ..models import Income
from utils.base_admin import BaseAdmin


@admin.register(Income)
class IncomeAdmin(BaseAdmin):
    list_display = ['id',  'trade', 'token', 'amount', 'is_maker']
    list_filter = ['token',]