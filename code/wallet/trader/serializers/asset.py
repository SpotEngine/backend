from utils.serializers import CustomUserModelSerializer
from ...models import Asset


class AssetSerializer(CustomUserModelSerializer):
    class Meta:
        model = Asset
        fields = ['token', 'free', 'id']
