import datetime
import random
import typing

from nucoro_currency.currencies.models import Currency


class MockClient(object):

    @staticmethod
    def _get_random_rate_value():
        units = random.randint(0, 99)
        decimals = random.randint(100000, 999999)
        return float(f"{units}.{decimals}")

    def get_exchange_rate_by_date(self, from_currency: str, to_currency: str, date: datetime.date) -> typing.Dict:
        data = {
            'source_currency': from_currency,
            'exchanged_currency': to_currency,
            'valuation_date': date.strftime("%Y-%m-%d"),
            'rate_value': self._get_random_rate_value()
        }
        return data

    def get_all_latest_exchange_rates(self, from_currency: str) -> typing.List[typing.Dict]:
        data = [
            {
                'source_currency': from_currency,
                'exchanged_currency': currency,
                'valuation_date': datetime.today().strftime("%Y-%m-%d"),
                'rate_value': self._get_random_rate_value()
            }
            for currency in Currency.objects.all().values_list("code", flat=True)
        ]
        return data
