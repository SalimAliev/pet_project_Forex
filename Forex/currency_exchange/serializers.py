from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Currencies, ExchangeRates


class CurrencieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = ['id', 'name', 'code', 'sign']


class ExchangeRatesSerializer(serializers.ModelSerializer):
    baseCurrency = CurrencieSerializer(source='base_currency_id', read_only=True)
    targetCurrency = CurrencieSerializer(source='target_currency_id', read_only=True)

    class Meta:
        model = ExchangeRates
        fields = ['id', 'baseCurrency', 'targetCurrency', 'rate']


    def validate(self, data):
        a = self.initial_data
        base_currency_code = self.initial_data.get('baseCurrencyCode')
        target_currency_code = self.initial_data.get('targetCurrencyCode')
        errors = {}

        if not base_currency_code:
            errors["baseCurrencyCode"] = "This field is required."

        if not target_currency_code:
            errors["targetCurrencyCode"] = "This field is required."

        # Проверка наличия валюты baseCurrency в базе данных
        try:
            data["base_currency_id"] = Currencies.objects.get(code=base_currency_code)
        except Currencies.DoesNotExist:
            errors["baseCurrencyField"] = "Invalid base currency."

        # Проверка наличия валюты targetCurrency в базе данных
        try:
            data["target_currency_id"] = Currencies.objects.get(code=target_currency_code)
        except Currencies.DoesNotExist:
            errors["targetCurrencyField"] = "Invalid target currency."

        if errors:
            raise serializers.ValidationError(errors)

        return data

    def create(self, validated_data):

        exchange_rate, created = ExchangeRates.objects.get_or_create(
            base_currency_id=validated_data['base_currency_id'],
            target_currency_id=validated_data['target_currency_id'],
            defaults={'rate': validated_data['rate']}
        )
        if not created:
            raise serializers.ValidationError("Exchange rate already exists.")

        return exchange_rate


class ExchangeSerializer(serializers.Serializer):
    baseCurrency = CurrencieSerializer(source='base_currency_id', read_only=True)
    targetCurrency = CurrencieSerializer(source='target_currency_id', read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        amount = int(self.context.get('amount'))
        rate = round(float(self.context.get('rate')), 3)
        representation['rate'] = rate
        representation['amount'] = amount
        representation['convertedAmount'] = round(amount*rate, 2)
        return representation


