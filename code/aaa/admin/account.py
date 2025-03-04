from django.contrib import admin

from utils.base_admin import BaseAdmin
from ..models import Account




@admin.register(Account)
class AccountAdmin(BaseAdmin):
    list_display = [
        "id",
        "user",
        "type",
        "is_active",
    ]
    list_filter = ["type", "is_active"] 
    search_fields = ["user__email"]

