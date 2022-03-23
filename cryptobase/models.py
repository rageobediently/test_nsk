from django.db import models


class Coin(models.Model):
    name = models.CharField(max_length=50, blank=True, verbose_name='Название монеты')

    def __str__(self):
        return self.name


class Value(models.Model):
    coin = models.ForeignKey('Coin', on_delete=models.CASCADE, related_name='value', verbose_name='Монета')
    time = models.DateTimeField(null=True, blank=True, verbose_name='Время')
    open_value = models.FloatField(blank=True, null=True, verbose_name='Открытие')
    high = models.FloatField(blank=True, null=True, verbose_name='High')
    low = models.FloatField(blank=True, null=True, verbose_name='Low')
    close = models.FloatField(blank=True, null=True, verbose_name='Закрытие')
    vwap = models.FloatField(blank=True, null=True, )
    volume = models.FloatField(blank=True, null=True, verbose_name='Объем')
    count = models.IntegerField(blank=True, null=True, verbose_name='Count')
    market = models.CharField(max_length=50, blank=True, null=True, verbose_name='Биржа')
    is_hours = models.BooleanField(default=True, null=True, verbose_name='Это час')

    def __str__(self):
        return f'Значение монеты {self.coin.name} от {self.time}'

    @property
    def json(self):
        resp = {
            'time': self.time,
            'close': self.close,
            'open': self.open_value,
            'high': self.high,
            'low': self.low,
            'volume': self.volume,
            'Exchange': self.market
        }
        return resp

