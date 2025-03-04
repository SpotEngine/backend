from django.contrib import admin
from ..models import PerpetualWallet
from utils.base_admin import BaseAdmin


@admin.register(PerpetualWallet)
class PerpetualWalletAdmin(BaseAdmin):
    list_display = ['id', 'account', 'token', 'free',]
    list_filter = ['token', ]