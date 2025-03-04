from utils.serializers import CustomModelSerializer
from ...models import PerpetualWallet


class PerpWalletSerializer(CustomModelSerializer):
    class Meta:
        model = PerpetualWallet
        fields = ['token', 'free',]

