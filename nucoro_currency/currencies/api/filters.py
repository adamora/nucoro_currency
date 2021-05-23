import django_filters

from nucoro_currency.currencies.models import CurrencyExchangeRate, Currency


class CurrencyExchangeRateFilter(django_filters.rest_framework.FilterSet):
    date_from = django_filters.DateFilter(field_name='valuation_date', lookup_expr="gte", label="Date from")
    date_to = django_filters.DateFilter(field_name='valuation_date', lookup_expr="lte", label="Date to")

    class Meta:
        model = CurrencyExchangeRate
        fields = ["source_currency"]

