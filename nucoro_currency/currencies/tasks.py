from pydoc import locate

from config import celery_app
from nucoro_currency.currencies.models import Provider
from nucoro_currency.currencies.utils.clients.currencies_methods import CurrenciesMethods


# @celery_app.task()
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    provider_instance = Provider.objects.get(slug=provider)
    klass = locate(provider_instance.path)
    CurrenciesMethods(klass()).get_exchange_rate_by_date(
        from_currency=source_currency, to_currency=exchanged_currency, date=valuation_date)
