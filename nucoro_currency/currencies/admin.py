from django.contrib import admin

from nucoro_currency.currencies.models import Provider


class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "path", "default", )
    search_fields = ("name", "slug", "path", )


admin.site.register(Provider, ProviderAdmin)
