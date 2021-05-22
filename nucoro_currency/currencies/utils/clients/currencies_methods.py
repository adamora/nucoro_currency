import datetime
import typing
from decimal import Decimal
from django.conf import settings
from django.db.models import QuerySet

from nucoro_currency.currencies.models import Currency, CurrencyExchangeRate
from nucoro_currency.currencies.utils.commons import get_dates_between_dates
from nucoro_currency.currencies.utils.interfaces.currencies import CurrenciesInterface


class CurrenciesMethods(object):
    client = None

    def __init__(self, client: CurrenciesInterface) -> None:
        super().__init__()
        self.client = client

    @staticmethod
    def _create_instance(data):
        required_fields = ['source_currency', 'exchanged_currency', 'valuation_date', 'rate_value']
        assert type(data) == dict and set(data.keys()) == set(required_fields)
        assert type(data['rate_value']) == Decimal
        assert type(data['valuation_date']) == datetime.date
        data['source_currency'] = Currency.objects.get(code=data['source_currency'])
        data['exchanged_currency'] = Currency.objects.get(code=data['exchanged_currency'])
        instance, created = CurrencyExchangeRate.objects.get_or_create(**data)
        return instance

    def get_exchange_rate_by_date(self, from_currency: str, to_currency: str,
                                  date: datetime.date) -> CurrencyExchangeRate:
        assert from_currency.upper() in settings.AVAILABLE_CURRENCIES
        assert to_currency.upper() in settings.AVAILABLE_CURRENCIES
        data = self.client.get_exchange_rate_by_date(from_currency, to_currency, date)
        return self._create_instance(data)

    def get_exchange_rates_by_date_range(self, from_currency: str, date_from: datetime.date,
                                         date_to: datetime.date) -> CurrencyExchangeRate:
        assert (type(date_from) == datetime.date) and (type(date_to) == datetime.date)
        id_list = []
        for to_currency in settings.AVAILABLE_CURRENCIES:
            id_list += [self.get_exchange_rate_by_date(from_currency, to_currency, date).id
                        for date in get_dates_between_dates(date_from, date_to)]
        return CurrencyExchangeRate.objects.filter(id__in=set(id_list))

    def get_all_latest_exchange_rates(self, from_currency: str) -> typing.Union[QuerySet, typing.List[CurrencyExchangeRate]]:
        data = self.client.get_all_latest_exchange_rates(from_currency)
        id_list = [self._create_instance(i).id for i in data]
        return CurrencyExchangeRate.objects.filter(id__in=set(id_list))

    def get_latest_exchange_rate(self, from_currency: str, to_currency: str) -> CurrencyExchangeRate:
        assert from_currency.upper() in settings.AVAILABLE_CURRENCIES
        assert to_currency.upper() in settings.AVAILABLE_CURRENCIES
        queryset = self.get_all_latest_exchange_rates(from_currency=from_currency)
        return queryset.filter(source_currency__code=from_currency, exchanged_currency__code=to_currency).last()
