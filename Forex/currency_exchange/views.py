from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CurrencieSerializer, ExchangeRatesSerializer, ExchangeSerializer
from .models import Currencies, ExchangeRates
from django.shortcuts import get_object_or_404


class CurrenciesViewSet(APIView):

    def get(self, request):
        currencies_data = Currencies.objects.all()
        return Response(CurrencieSerializer(currencies_data, many=True).data)

    def post(self, request):
        serializer = CurrencieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CurrencyView(APIView):

    def get(self, request, code):
        currency = get_object_or_404(Currencies, code=code)
        return Response(CurrencieSerializer(currency).data)


class HandleMissingCurrencyCode(APIView):

    def get(self, request):
        return Response({'error': 'The currency code is missing in the address'}, status=400)


class ExchangeRatesViewSet(APIView):
    def get(self, request):
        # ПРОВЕРИТЬ ОПТИМИЗАЦИЮ
        exchange_rates_data = ExchangeRates.objects.all()
        return Response(ExchangeRatesSerializer(exchange_rates_data, many=True).data)

    def post(self, request):
        serializer = ExchangeRatesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ExchangeRateView(APIView):
    def get(self, request, base_currency_code, target_currency_code):
        exchange_rate = get_object_or_404(ExchangeRates, base_currency_id__code=base_currency_code,
                                          target_currency_id__code=target_currency_code)
        return Response(ExchangeRatesSerializer(exchange_rate).data)

    def patch(self, request, base_currency_code, target_currency_code):
        exchange_rate = get_object_or_404(ExchangeRates, base_currency_id__code=base_currency_code,
                                          target_currency_id__code=target_currency_code)
        data = request.data
        data['baseCurrencyCode'] = base_currency_code
        data['targetCurrencyCode'] = target_currency_code
        serializer = ExchangeRatesSerializer(data=data, instance=exchange_rate)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"asd": serializer.data})


class ExchangeView(APIView):
    def get(self, request):
        from_code = request.GET.get('from')
        to_code = request.GET.get('to')
        amount = request.GET.get('amount')

        if from_code=='USD':
            exchange_rate = get_object_or_404(ExchangeRates, base_currency_id__code=from_code,
                                              target_currency_id__code=to_code)
            serializer = ExchangeSerializer(exchange_rate, context={'amount': amount, 'rate': exchange_rate.rate})
            return Response(serializer.data)

        elif to_code=='USD':
            exchange_rate = get_object_or_404(ExchangeRates, base_currency_id__code=to_code,
                                              target_currency_id__code=from_code)
            serializer = ExchangeSerializer(exchange_rate, context={'amount': amount, 'rate': 1/exchange_rate.rate})
            return Response(serializer.data)
        else:
            exchange_rate_to = get_object_or_404(ExchangeRates, base_currency_id__code='USD',
                                              target_currency_id__code=to_code)
            exchange_rate_from = get_object_or_404(ExchangeRates, base_currency_id__code='USD',
                                              target_currency_id__code=from_code)
            rate = exchange_rate_to.rate/exchange_rate_from.rate

            exchange_rate = ExchangeRates(base_currency_id=exchange_rate_from.target_currency_id, target_currency_id=exchange_rate_to.target_currency_id, rate=rate)

            return Response(ExchangeSerializer(exchange_rate, context={'amount': amount, 'rate': exchange_rate.rate}).data)


class HandleMissingCurrenciesCodes(APIView):

    def get(self, request):
        return Response({'error': 'Currency codes of the pair are missing in the address'}, status=400)