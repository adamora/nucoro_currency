import datetime
from pydoc import locate
from typing import Any

from django.conf import settings
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from nucoro_currency.currencies.api.filters import CurrencyExchangeRateFilter, CalculateExchangeFilter
from nucoro_currency.currencies.api.serializers import CurrencyExchangeRateSerializer, CurrencyExchangeSerializer, \
    CurrencyExchangeQueryParamsSerializer
from nucoro_currency.currencies.models import CurrencyExchangeRate, Currency
from nucoro_currency.currencies.utils.clients.currencies_methods import CurrenciesMethods


class ExtendedGenericViewSet(GenericViewSet):
    required_query_params = None
    required_query_params_serializer = None

    provider = "Fixer"
    currency_client = None

    def _set_currency_client(self):
        klass = locate(settings.PROVIDERS[self.provider])
        self.currency_client = CurrenciesMethods(klass())

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not self.currency_client:
            self._set_currency_client()

    def check_query_params(self):
        query_obj = self.request.GET
        not_filled_attrs = [i for i in self.required_query_params or list() if not query_obj.get(i)]
        if not_filled_attrs:
            raise ValidationError({i: ["This query param is required"] for i in not_filled_attrs})
        if self.required_query_params_serializer:
            self.required_query_params_serializer(data=self.request.GET).is_valid(raise_exception=True)

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_query_params()


class CurrencyExchangeRateView(ExtendedGenericViewSet, mixins.ListModelMixin):
    """Service to retrieve a List of currency rates for a specific time period"""
    serializer_class = CurrencyExchangeRateSerializer
    queryset = CurrencyExchangeRate.objects.all()
    permission_classes = (AllowAny, )
    filterset_class = CurrencyExchangeRateFilter

    def process_query_params(self):
        data = None
        required_attrs = ['source_currency', 'date_from', 'date_to']  # Required args to call external service
        query_obj = self.request.GET
        if not [i for i in required_attrs if not query_obj.get(i)]:
            data = {
                'from_currency': Currency.objects.get(id=query_obj['source_currency']).code,
                'date_from': datetime.datetime.strptime(query_obj['date_from'], "%Y-%m-%d").date(),
                'date_to': datetime.datetime.strptime(query_obj['date_to'], "%Y-%m-%d").date(),
            }
        return data

    def list(self, request, *args, **kwargs):
        """Service to retrieve a List of currency rates for a specific time period"""
        data = self.process_query_params()
        if data:
            self.currency_client.get_exchange_rates_by_date_range(**data)
        return super().list(request, *args, **kwargs)


class CalculateExchangeView(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Service that Calculates (latest) amount in a currency exchanged into a different currency.
    URL example: http://localhost:8000/api/v1/calculate-exchange?source_currency=EUR&exchanged_currency=USD&amount=100
    """
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeSerializer
    permission_classes = [AllowAny]
    filterset_class = CalculateExchangeFilter

    required_query_params = ['source_currency', 'exchanged_currency', 'amount']
    required_query_params_serializer = CurrencyExchangeQueryParamsSerializer

    def list(self, request, *args, **kwargs):
        """
        Service that Calculates (latest) amount in a currency exchanged into a different currency.
        URL example: http://localhost:8000/api/v1/calculate-exchange?source_currency=EUR&exchanged_currency=USD&amount=100
        """
        instance = self.currency_client.get_latest_exchange_rate(
            from_currency=request.GET['source_currency'],
            to_currency=request.GET['exchanged_currency'],
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

