import json
import requests
from config import currency

class ConversationException(Exception):
    pass

class Converter:
    @staticmethod
    def convert(in_currency, out_currency, amount):
        if in_currency == out_currency:
            raise ConversationException(f'значения валют совпадают {out_currency}')
        if in_currency not in currency or out_currency not in currency:
            raise ConversationException('Нет такой валюты')
        try:
            amount_float = float(amount)
        except:
            raise ConversationException('это не число')
        if amount_float <= 0:
            raise ConversationException(f'отрицательное значение {amount_float}')

        res = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={currency[in_currency]}&tsyms={currency[out_currency]}')
        total = json.loads(res.content)[currency[out_currency]] * amount_float
        return total

