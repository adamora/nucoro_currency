from django.contrib import admin
from django.db import models
from django.urls import path

from nucoro_currency.currencies.models import Provider
from nucoro_currency.currencies.views import ExchangeRateEvolutionView


class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "path", "default", )
    search_fields = ("name", "slug", "path", )


admin.site.register(Provider, ProviderAdmin)


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
