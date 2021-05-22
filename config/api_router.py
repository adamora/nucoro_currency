from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from nucoro_currency.currencies.api.views import CurrencyExchangeRateView, CalculateExchangeView
from nucoro_currency.users.api.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter(trailing_slash=False)
else:
    router = SimpleRouter()


router.register("currency-exchange-rates", CurrencyExchangeRateView, basename="currency-exchange-rates")
router.register("calculate-exchange", CalculateExchangeView, basename="calculate-exchange")


app_name = "api_v1"
urlpatterns = router.urls
