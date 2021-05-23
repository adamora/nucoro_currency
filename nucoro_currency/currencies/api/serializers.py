from rest_framework import serializers

from nucoro_currency.currencies.models import CurrencyExchangeRate, Currency


class CurrencyExchangeRateSerializer(serializers.ModelSerializer):
    source_currency = serializers.CharField(source='source_currency.code')
    exchanged_currency = serializers.CharField(source='exchanged_currency.code')

    class Meta:
        model = CurrencyExchangeRate
        fields = [
            "source_currency", "exchanged_currency", "valuation_date", "rate_value"
        ]


class CurrencyExchangeSerializer(CurrencyExchangeRateSerializer):
    source_amount = serializers.SerializerMethodField()
    exchanged_amount = serializers.SerializerMethodField()

    class Meta(CurrencyExchangeRateSerializer.Meta):
        fields = CurrencyExchangeRateSerializer.Meta.fields + ["source_amount", "exchanged_amount"]

    def get_source_amount(self, obj):
        return float(self.context['request'].GET['amount'])

    def get_exchanged_amount(self, obj):
        return round(float(self.context['request'].GET['amount']) * float(obj.rate_value), 6)


class CurrencyExchangeQueryParamsSerializer(serializers.Serializer):
    source_currency = serializers.ChoiceField(required=True, choices=Currency.objects.all().values_list("code", "code"))
    exchanged_currency = serializers.ChoiceField(required=True, choices=Currency.objects.all().values_list("code", "code"))
    amount = serializers.DecimalField(required=True, decimal_places=6, max_digits=999999999)


class TWRQueryParamsSerializer(CurrencyExchangeQueryParamsSerializer):
    date = serializers.DateField(required=True)
