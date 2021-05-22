import abc
import datetime
import typing


class CurrenciesInterface(abc.ABC):

    @abc.abstractmethod
    def get_exchange_rate_by_date(self, from_currency: str, to_currency: str, date: datetime.date) -> typing.Dict: pass

    @abc.abstractmethod
    def get_all_latest_exchange_rates(self, from_currency: str) -> typing.List[typing.Dict]: pass
