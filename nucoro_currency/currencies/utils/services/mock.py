import datetime
import random
import typing
from decimal import Decimal

from nucoro_currency.currencies.models import Currency


class MockClient(object):

    @staticmethod
    def _get_random_rate_value():
        units = random.randint(0, 99)
        decimals = random.randint(100000, 999999)
        return round(Decimal(float(f"{units}.{decimals}")), 6)

    def get_exchange_rate_by_date(self, from_currency: str, to_currency: str, date: datetime.date) -> typing.Dict:
        data = {
            'source_currency': from_currency,
            'exchanged_currency': to_currency,
            'valuation_date': date,
            'rate_value': self._get_random_rate_value()
        }
        return data

    def get_all_latest_exchange_rates(self, from_currency: str) -> typing.List[typing.Dict]:
        data = [
            {
                'source_currency': from_currency,
                'exchanged_currency': currency,
                'valuation_date': datetime.date.today(),
                'rate_value': self._get_random_rate_value()
            }
            for currency in Currency.objects.all().values_list("code", flat=True)
        ]
        return data
