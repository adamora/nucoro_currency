from pydoc import locate

from django.conf import settings

from config import celery_app
from nucoro_currency.currencies.utils.clients.currencies_methods import CurrenciesMethods


# @celery_app.task()
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    assert provider in ["Fixer", "Mock"]
    klass = locate(settings.PROVIDERS[provider])
    CurrenciesMethods(klass()).get_exchange_rate_by_date(
        from_currency=source_currency, to_currency=exchanged_currency, date=valuation_date)
