import datetime
from pydoc import locate
from typing import Any

from rest_framework import mixins
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from nucoro_currency.currencies.api.filters import CurrencyExchangeRateFilter
from nucoro_currency.currencies.api.serializers import CurrencyExchangeRateSerializer, CurrencyExchangeSerializer, \
    CurrencyExchangeQueryParamsSerializer, TWRQueryParamsSerializer, UploadFileDataSerializer
from nucoro_currency.currencies.models import CurrencyExchangeRate, Currency, Provider
from nucoro_currency.currencies.tasks import bulk_exchange_data_creation
from nucoro_currency.currencies.utils.clients.currencies_methods import CurrenciesMethods
from nucoro_currency.currencies.utils.commons import twr_formula


class ExtendedGenericViewSet(GenericViewSet):
    required_query_params = None
    required_query_params_serializer_class = None
    required_query_params_serializer = None  # This attr sets automatically

    currency_client = None

    def _set_currency_client(self):
        klass = locate(Provider.objects.get_default().path)
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
        if self.required_query_params_serializer_class:
            serializer = self.required_query_params_serializer_class(data=self.request.GET)
            serializer.is_valid(raise_exception=True)
            self.required_query_params_serializer = serializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.check_query_params()


class CurrencyExchangeRateView(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Service to retrieve a List of currency rates for a specific time period
    URL example: http://localhost:8000/api/v1/currency-exchange-rates?source_currency=1&date_from=2021-05-21&date_to=2021-05-22
    """
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

    required_query_params = ['source_currency', 'exchanged_currency', 'amount']
    required_query_params_serializer_class = CurrencyExchangeQueryParamsSerializer

    # Better using @action decorator, but it does not document on API ROOT
    def list(self, request, *args, **kwargs):
        instance = self.currency_client.get_latest_exchange_rate(
            from_currency=request.GET['source_currency'],
            to_currency=request.GET['exchanged_currency'],
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TWRView(ExtendedGenericViewSet, mixins.ListModelMixin):
    """
    Service to retrieve time-weighted rate of return for any given amount invested from a currency into another one from given date until today:
    URL example: http://localhost:8000/api/v1/twr?source_currency=EUR&exchanged_currency=USD&amount=100&date=2021-05-21
    """
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = CurrencyExchangeSerializer
    permission_classes = [AllowAny]

    required_query_params = ['source_currency', 'exchanged_currency', 'amount', 'date']
    required_query_params_serializer_class = TWRQueryParamsSerializer

    # Better using @action decorator, but it does not document on API ROOT
    def list(self, request, *args, **kwargs):
        query_params = self.required_query_params_serializer.validated_data
        initial_instance = self.currency_client.get_exchange_rate_by_date(
            from_currency=query_params['source_currency'],
            to_currency=query_params["exchanged_currency"],
            date=query_params["date"]
        )
        final_instance = self.currency_client.get_latest_exchange_rate(
            from_currency=query_params['source_currency'],
            to_currency=query_params["exchanged_currency"],
        )
        data = twr_formula(
            initial_rate=initial_instance.rate_value, final_rate=final_instance.rate_value,
            amount=query_params['amount']
        )
        return Response({
            "twr": round(data, 6),
            "twr_percentage": f"{round(data * 100, 6)}%"
        })


class UploadFileDataView(GenericViewSet, mixins.CreateModelMixin):
    """
    Batch procedure to retrieve exchange rates.
    Mechanism to ingest real-ish exchange rate data from a file in any format
    """
    queryset = CurrencyExchangeRate.objects.all()
    serializer_class = UploadFileDataSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        decoded_file = serializer.validated_data['file'].read().decode('utf-8')
        bulk_exchange_data_creation.apply_async((decoded_file, ))
