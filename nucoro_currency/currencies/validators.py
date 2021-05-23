from pydoc import locate

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from nucoro_currency.currencies.utils.interfaces.currencies import CurrenciesInterface


def validate_provider_path(value):
    klass = locate(value)
    if not (klass and issubclass(klass, CurrenciesInterface)):
        raise ValidationError(
            _("Path is not a subclass off %(module)s.%(class_name)s"),
            params={
                'module': CurrenciesInterface.__module__,
                'class_name': CurrenciesInterface.__qualname__
            }
        )
