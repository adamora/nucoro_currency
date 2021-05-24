import datetime
import json
from pydoc import locate
from typing import Any, Dict

from django.views.generic import TemplateView

from nucoro_currency.currencies.models import CurrencyExchangeRate, Currency, Provider
from nucoro_currency.currencies.utils.clients.currencies_methods import CurrenciesMethods
from nucoro_currency.currencies.utils.commons import random_color


class ExchangeRateEvolutionView(TemplateView):
    template_name = "admin/exchange_rate_evolution.html"
    queryset = CurrencyExchangeRate.objects.all()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        days = int(self.request.GET.get("days", 7)) - 1
        currency_client = CurrenciesMethods(locate(Provider.objects.get_default().path)())
        now = datetime.date.today()
        date_from = now - datetime.timedelta(days=days)
        queryset = currency_client.get_exchange_rates_by_date_range(
            from_currency="EUR", date_from=date_from, date_to=now).order_by('valuation_date')
        labels = list(
            dict.fromkeys(
                list(
                    map(lambda x: x.strftime("%Y-%m-%d"), queryset.values_list("valuation_date", flat=True))
                )
            )
        )
        self.extra_context = {
            "labels": json.dumps(labels),
            "json_data": json.dumps(
                [
                    {
                        'label': f"EUR-{i.code}",
                        'data': list(map(lambda x: float(x), queryset.filter(
                            source_currency__code="EUR", exchanged_currency__code=i.code
                        ).values_list("rate_value", flat=True))),
                        'borderColor': random_color(),
                        'backgroundColor': random_color()
                    } for i in Currency.objects.all().order_by("id")
                ]
            ),
        }
        return super().get_context_data(**kwargs)
