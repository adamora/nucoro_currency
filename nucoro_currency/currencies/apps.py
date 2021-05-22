from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CurrenciesConfig(AppConfig):
    name = "nucoro_currency.currencies"
    verbose_name = _("Currencies")

    def ready(self):
        try:
            import nucoro_currency.currencies.signals  # noqa F401
        except ImportError:
            pass
