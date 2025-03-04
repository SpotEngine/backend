from utils.serializers import CustomAccountModelSerializer
from ...models import Symbol


class SymbolSerializer(CustomAccountModelSerializer):
    class Meta:
        model = Symbol
        exclude = ['priority']
