from utils.serializers import CustomAccountModelSerializer
from ...models import Token


class TokenSerializer(CustomAccountModelSerializer):
    class Meta:
        model = Token
        fields = ['ticker', 'name', 'supply', 'is_active']
        extra_kwargs = {
            'ticker': {'required': True},
            'name': {'required': True},
            'supply': {'required': True},
            'is_active': {'read_only': True},
        }


    def create(self, validated_data):
        obj = Token.create(
            account_id=self.account_id,
            ticker=validated_data['ticker'],
            name=validated_data['name'],
            supply=validated_data['supply'],
        )
        return obj