from django.db import models


class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=20, db_index=True)
    symbol = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.code


class CurrencyExchangeRate(models.Model):
    source_currency = models.ForeignKey(Currency,
                                        related_name='exchanges',
                                        on_delete=models.CASCADE)
    exchanged_currency = models.ForeignKey(Currency,
                                           on_delete=models.CASCADE)
    valuation_date = models.DateField(db_index=True)
    rate_value = models.DecimalField(db_index=True, decimal_places=6, max_digits=18)


class Provider(models.Model):
    name = models.CharField(max_length=20, db_index=True, help_text="Provider name")
    slug = models.SlugField(unique=True, help_text="Unique slug identifier for a provider")
    path = models.CharField(max_length=250, help_text="Path to a provider adapter class")
    default = models.BooleanField(default=False, help_text="Provider priority")
