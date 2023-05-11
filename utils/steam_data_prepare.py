import json

from typing import List

from currency_converter import CurrencyConverter


def steam_data_prepare(data: str) -> List[float]:
    '''
    :param data: Строка с данными steam market.
    :return: Список цен в йенах.
    '''

    data = json.loads(data)

    yen_list = []

    c = CurrencyConverter()

    for item in data:
        yen_list.append(c.convert(item[1], 'USD', 'CNY'))

    return yen_list
