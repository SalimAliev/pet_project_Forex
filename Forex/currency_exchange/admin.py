from django.contrib import admin
from .models import Currencies, ExchangeRates


myModels = [Currencies, ExchangeRates]

admin.site.register(myModels)