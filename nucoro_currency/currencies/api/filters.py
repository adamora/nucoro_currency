import django_filters

from nucoro_currency.currencies.models import CurrencyExchangeRate, Currency


class CurrencyExchangeRateFilter(django_filters.rest_framework.FilterSet):
    date_from = django_filters.DateFilter(field_name='valuation_date', lookup_expr="gte", label="Date from")
    date_to = django_filters.DateFilter(field_name='valuation_date', lookup_expr="lte", label="Date to")

    class Meta:
        model = CurrencyExchangeRate
        fields = ["source_currency"]


class CalculateExchangeFilter(django_filters.rest_framework.FilterSet):
    source_currency = django_filters.ChoiceFilter(choices=Currency.objects.values_list("code", "name"))
    exchanged_currency = django_filters.ChoiceFilter(choices=Currency.objects.values_list("code", "name"))
    amount = django_filters.NumberFilter()

    def filter_queryset(self, queryset):
        """Avoid any filter options"""
        return queryset

