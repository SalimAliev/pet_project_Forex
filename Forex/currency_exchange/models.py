from django.db import models


class Currencies(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    sign = models.CharField(max_length=5)

    def __str__(self):
        return str(self.code)


class ExchangeRates(models.Model):
    class Meta:
        unique_together = ('base_currency_id', 'target_currency_id')
    base_currency_id = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='base_currency')
    target_currency_id = models.ForeignKey(Currencies, on_delete=models.CASCADE, related_name='target_currency')
    rate = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(f'{self.base_currency_id}-{self.target_currency_id}')
