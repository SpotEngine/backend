import django_filters
from ...models import PerpetualWallet

class PerpWalletFilter(django_filters.FilterSet):
    class Meta:
        model = PerpetualWallet
        fields = ['token__ticker']