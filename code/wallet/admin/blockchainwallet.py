from django.contrib import admin
from ..models import BlockchainWallet
from utils.base_admin import BaseAdmin

@admin.register(BlockchainWallet)
class BlockchainWalletAdmin(BaseAdmin):
    list_display = ['id', 'user', 'wallet_address']