import json
from lxml import html
import requests

from config import APIKEY

currencies = dict()


class ConversionException(Exception):
    pass


def get_currencies():
    res = requests.get('https://www.banki.ru/products/currency/cb/')
    tree = html.fromstring(res.text)
    tbody = tree.xpath("/html/body/div[1]/div[1]/main/div[2]/table/tbody").pop()
    currencies['Российский рубль'] = 'RUB'
    for tr in tbody:
        currencies[tr.attrib['data-currency-name']] = tr.attrib['data-currency-code']


class CurrenciesConverter:

    @staticmethod
    def get_price(values: list) -> str:

        if len(values) != 3:
            if len(values) == 2:
                base, quote = values
                amount = 1
            else:
                raise ConversionException('Введено неверное количество параметров')
        else:
            base, quote, amount = values

        if base == quote:
            raise ConversionException(f'Нельзя конвертировать одноименные валюты: {base}')

        if len(currencies) == 0:
            get_currencies()

        if base not in currencies.values():
            if base.upper() not in currencies.values():
                raise ConversionException(f'Не найден код валюты для конвертации: {base}')
            else:
                base = base.upper()

        if quote not in currencies.values():
            if quote.upper() not in currencies.values():
                raise ConversionException(f'Не найден код валюты, в которую осуществляется конвертация: {quote}')
            else:
                quote = quote.upper()

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество валюты: {amount}')

        url = f'https://api.apilayer.com/exchangerates_data/convert?' \
              f'apikey={APIKEY}&from={base}&to={quote}&amount={amount}'
        response = requests.get(url)
        total_base = json.loads(response.content)['result']
        answer = f'Цена {amount} {base} в {quote} составляет: {total_base}'

        return answer

    @staticmethod
    def show_currencies():
        if len(currencies) == 0:
            get_currencies()
        currencies_list = 'Доступные валюты (Буквенный код / Наименование):\n\n'
        for key in currencies.keys():
            currencies_list += f'{currencies[key]} - {key}\n'
        return currencies_list
