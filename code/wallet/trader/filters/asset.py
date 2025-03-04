import django_filters
from ...models import Asset
import django_filters


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class AssetFilter(django_filters.FilterSet):
    token = CharInFilter(field_name='token__ticker', lookup_expr='in')
    class Meta:
        model = Asset
        fields = ['token']

