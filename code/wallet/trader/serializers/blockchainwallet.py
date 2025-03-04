from utils.serializers import CustomUserModelSerializer
from ...models import BlockchainWallet


class BlockchainWalletSerializer(CustomUserModelSerializer):
    class Meta:
        model = BlockchainWallet
        exclude = ['user', 'is_active']
