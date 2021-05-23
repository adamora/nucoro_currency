from django.contrib import admin
from django.db import models
from django.urls import path

from nucoro_currency.currencies.models import Provider, CurrencyExchangeRate, Currency
from nucoro_currency.currencies.views import ExchangeRateEvolutionView


admin.site.register(Currency)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "path", "default", )
    search_fields = ("name", "slug", "path", )


admin.site.register(Provider, ProviderAdmin)


class CurrencyExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("source_currency_code", "exchanged_currency_code", "valuation_date", "rate_value", )
    search_fields = ("exchanged_currency__code", "valuation_date", "rate_value")

    def source_currency_code(self, obj):
        return obj.source_currency.code
    source_currency_code.short_description = 'Source Currency'
    source_currency_code.admin_order_field = 'source_currency__code'

    def exchanged_currency_code(self, obj):
        return obj.exchanged_currency.code
    exchanged_currency_code.short_description = 'Exchanged Currency'
    exchanged_currency_code.admin_order_field = 'exchanged_currency__code'


admin.site.register(CurrencyExchangeRate, CurrencyExchangeRateAdmin)


class DummyModel(models.Model):

    class Meta:
        verbose_name_plural = 'Exchange Rate Evolution'
        app_label = 'currencies'
        managed = False


class DummyModelAdmin(admin.ModelAdmin):
    model = DummyModel

    def get_urls(self):
        view_name = '{}_{}_changelist'.format(
            self.model._meta.app_label, self.model._meta.model_name)
        return [
            path('exchange-rate-evolution/', ExchangeRateEvolutionView.as_view(), name=view_name),
        ]


admin.site.register(DummyModel, DummyModelAdmin)
