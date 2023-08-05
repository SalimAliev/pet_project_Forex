from django.contrib import admin
from django.urls import path

from currency_exchange.views import CurrenciesViewSet, CurrencyView, HandleMissingCurrencyCode, ExchangeRatesViewSet, ExchangeRateView, HandleMissingCurrenciesCodes, ExchangeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/currencies/', CurrenciesViewSet.as_view()),
    path('api/currency/<str:code>/', CurrencyView.as_view()),
    path('api/currency/', HandleMissingCurrencyCode.as_view()),

    path('api/exchange/', ExchangeView.as_view()),
    path('api/exchangeRates/', ExchangeRatesViewSet.as_view()),
    path('api/exchangeRate/<str:base_currency_code>-<str:target_currency_code>/', ExchangeRateView.as_view()),
    path('api/exchangeRate/', HandleMissingCurrenciesCodes.as_view()),

]
