import csv
import io
from decimal import Decimal

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    exchanged_currency = serializers.ChoiceField(required=True,
                                                 choices=Currency.objects.all().values_list("code", "code"))
    amount = serializers.DecimalField(required=True, decimal_places=6, max_digits=999999999)


class TWRQueryParamsSerializer(CurrencyExchangeQueryParamsSerializer):
    date = serializers.DateField(required=True)


class CurrencyExchangeRateCreateSerializer(serializers.ModelSerializer):
    source_currency = serializers.ChoiceField(required=True, choices=Currency.objects.all().values_list("code", "code"))
    exchanged_currency = serializers.ChoiceField(required=True,
                                                 choices=Currency.objects.all().values_list("code", "code"))
    rate_value = serializers.CharField(required=True)

    class Meta:
        model = CurrencyExchangeRate
        fields = [
            "source_currency", "exchanged_currency", "valuation_date", "rate_value"
        ]

    @staticmethod
    def _common_currency_validation(value):
        try:
            return Currency.objects.get(code=value)
        except Currency.DoesNotExist:
            raise ValidationError("Invalid currency")

    def validate_source_currency(self, value):
        return self._common_currency_validation(value)

    def validate_exchanged_currency(self, value):
        return self._common_currency_validation(value)

    def validate_rate_value(self, value):
        return round(Decimal(value.replace(".", "").replace(",", ".")), 6)

    def create(self, validated_data):
        try:
            instance = self.Meta.model.objects.get(**validated_data)
        except self.Meta.model.DoesNotExist:
            instance = super().create(validated_data)
        return instance


class UploadFileDataSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ["file"]

    def validate_file(self, value):
        if value.content_type not in ["text/csv"]:
            raise ValidationError("Invalid file type")
        decoded_file = value.read().decode('utf-8')
        with io.StringIO(decoded_file) as file:
            reader = csv.reader(file)
            csv_headings = next(reader)
            if set(csv_headings) != set(CurrencyExchangeRateCreateSerializer.Meta.fields):
                raise ValidationError("Invalid file content")
        value.seek(0)
        return value

    def to_representation(self, instance):
        return {"status": "successful"}
