import json
import requests
from config import headers, exchanges

class APIException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(base: str, sym: str, amount: str):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://api.apilayer.com/fixer/latest?symbols={sym_key}&base={base_key}", headers=headers)
        data = json.loads(r.content)[sym_key]
        return data

