from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "nucoro_currency.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import nucoro_currency.users.signals  # noqa F401
        except ImportError:
            pass
