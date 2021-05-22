import datetime
import typing
from decimal import Decimal

from django.conf import settings

from nucoro_currency.currencies.utils.interfaces.currencies import CurrenciesInterface
from nucoro_currency.currencies.utils.services.fixer import FixerClient


class FixerAdapter(CurrenciesInterface):
    service = None

    def __init__(self, service: FixerClient = None) -> None:
        super().__init__()
        self.service = service or FixerClient()

    def get_exchange_rate_by_date(self, from_currency: str, to_currency: str, date: datetime.date) -> typing.Dict:
        response_data = self.service.historical(date=date, base=from_currency, symbols=[to_currency])
        data = {
            'source_currency': from_currency,
            'exchanged_currency': to_currency,
            'valuation_date': date,
            'rate_value': round(Decimal(response_data['rates'][to_currency]), 6)
        }
        return data

    def get_all_latest_exchange_rates(self, from_currency: str) -> typing.List[typing.Dict]:
        response_data = self.service.latest(base=from_currency, symbols=settings.AVAILABLE_CURRENCIES)
        data = [
            {
                'source_currency': from_currency,
                'exchanged_currency': currency,
                'valuation_date': datetime.datetime.strptime(response_data['date'], "%Y-%m-%d").date(),
                'rate_value': round(Decimal(rate_value), 6)
            }
            for currency, rate_value in response_data['rates'].items()
        ]
        return data
