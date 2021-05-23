import datetime
import random
import typing

from nucoro_currency.currencies.utils.interfaces.currencies import CurrenciesInterface
from nucoro_currency.currencies.utils.services.mock import MockClient


class MockAdapter(CurrenciesInterface):
    def __init__(self, service: MockClient = None) -> None:
        super().__init__()
        self.service = service or MockClient()

    def get_exchange_rate_by_date(self, from_currency: str, to_currency: str, date: datetime.date) -> typing.Dict:
        return self.service.get_exchange_rate_by_date(from_currency, to_currency, date)

    def get_all_latest_exchange_rates(self, from_currency: str) -> typing.List[typing.Dict]:
        return self.service.get_all_latest_exchange_rates(from_currency)
