from django.core.management.base import BaseCommand
from cryptobase.models import Value, Coin
import datetime
import json
from django.utils import timezone
import requests
import pytz

BASE_URL_KRAKEN = 'https://api.kraken.com/0/public/OHLC?'
BASE_URL_BITFINEX = ''
BASE_TOKENS = [
    'BTCUSD',
    'ETHUSD',
    'XRPUSD',
    'XRPEUR'
]


class Command(BaseCommand):
    help = 'updating coins database'

    def handle(self, *args, **options):
        main()


def main():
    get_from_market('kraken')
    # get_from_market('bitfinex')


def get_from_market(market):
    for coin in BASE_TOKENS:
        obj, created = Coin.objects.get_or_create(name=coin)
        if market == 'kraken':
            data = get_hour_last_30_days(coin, BASE_URL_KRAKEN)
            if data is None:
                print('Не найдена пара')
                continue
            min_data = get_data_of_mins(coin, BASE_URL_KRAKEN)
        elif market == 'bitfinex':
            data = get_hour_last_30_days(coin, BASE_URL_BITFINEX)
            if data is None:
                print('Не найдена пара')
                continue
            min_data = get_data_of_mins(coin, BASE_URL_KRAKEN)
        else:
            break
        if created:
            for value in data:
                insert_data(value, obj, market)
            for value in min_data:
                insert_data(value, obj, market, is_hours=False)
        else:
            last_time = obj.value.filter(is_hours=True).order_by('time').last()
            if last_time is not None:
                for value in data:

                    if last_time.time < timezone.datetime.fromtimestamp(value[0], tz=pytz.UTC):
                        insert_data(value, obj, market)
                for value in min_data:
                    insert_data(value, obj, market, is_hours=False)
            else:
                for value in data:
                    insert_data(value, obj, market)
                for value in min_data:
                    insert_data(value, obj, market, is_hours=False)


def get_data_of_mins(pair, url):
    response = get_one_currency(url, pair, 1)
    return response.get('result', 'no').get(list(response.get('result').keys())[0])


def insert_data(value, obj, market, is_hours=True):
    val_obj, cr = Value.objects.get_or_create(
        time=datetime.datetime.fromtimestamp(value[0]),
        coin=obj,
        market=market
    )
    val_obj.open_value = value[1]
    val_obj.high = value[2]
    val_obj.low = value[3]
    val_obj.close = value[4]
    val_obj.vwap = value[5]
    val_obj.volume = value[6]
    val_obj.count = value[7]
    val_obj.is_hours = is_hours
    val_obj.save()


def get_hour_last_30_days(pair, url):
    response = get_one_currency(url, pair, 60)
    return response.get('result', 'no').get(list(response.get('result').keys())[0])


def get_one_currency(base_url, name, interval):
    url = base_url + 'pair=' + name + '&' + 'interval=' + str(interval)
    resp = requests.get(url)
    return resp.json()
