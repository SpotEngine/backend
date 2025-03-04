from utils.serializers import CustomAccountModelSerializer, serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from ...models import Symbol


class SpotTraderSymbolSerializer(CustomAccountModelSerializer):
    symbol = serializers.SerializerMethodField()
    class Meta:
        model = Symbol
        fields = ['symbol', 'base', 'quote', 'lot_size', 'tick_size']
        # extra_lwargs = {
        #     'symbol': {'read_only': True, 'required': False},
        # }
        validators = [
            UniqueTogetherValidator(
                queryset=Symbol.objects.all(),
                fields=['base', 'quote'],
                message="Symbol with this base and quote already exist."
            )
        ]    

    def get_symbol(self, instance):
        return instance.symbol
    
    def validate(self, attrs):
        base = attrs['base']
        quote = attrs['quote']
        if base == quote:
            raise ValidationError({"quote": ["quote and base can't be the same"]})
        return super().validate(attrs)
    
    def create(self, validated_data):
        obj = Symbol.create(
            account_id=self.account_id,
            base=validated_data['base'],
            quote=validated_data['quote'],
            lot_size=validated_data['lot_size'],
            tick_size=validated_data['tick_size'],
        )
        return obj