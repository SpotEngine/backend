import django_filters


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass
class OrderFilter(django_filters.FilterSet):
    status = CharInFilter(field_name='status', lookup_expr='in')
    # uncategorized = django_filters.BooleanFilter(field_name='category', lookup_expr='isnull')
