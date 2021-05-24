import csv
import io
from pydoc import locate

from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from config import celery_app
from nucoro_currency.currencies.api.serializers import CurrencyExchangeRateCreateSerializer
from nucoro_currency.currencies.models import Provider
from nucoro_currency.currencies.utils.clients.currencies_methods import CurrenciesMethods


logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(hour=0, minute=0)), name="daily_exchange_rate_data")
def get_daily_exchange_rate():
    provider_instance = Provider.objects.get_default()
    klass = locate(provider_instance.path)
    CurrenciesMethods(klass()).get_all_latest_exchange_rates(
        from_currency="EUR"
    )


@celery_app.task
def get_exchange_rate_data(source_currency, exchanged_currency, valuation_date, provider):
    provider_instance = Provider.objects.get(slug=provider)
    klass = locate(provider_instance.path)
    CurrenciesMethods(klass()).get_exchange_rate_by_date(
        from_currency=source_currency, to_currency=exchanged_currency, date=valuation_date)


@celery_app.task
def bulk_exchange_data_creation(data):
    with io.StringIO(data) as file:
        reader = csv.DictReader(file)
        for row in reader:
            serializer = CurrencyExchangeRateCreateSerializer(data=row)
            if serializer.is_valid():
                serializer.save()
