import json

from currency_converter import CurrencyConverter


def steam_data_prepare(data: str, steam_resample: int) -> tuple[list]:
    '''
    :param data: Строка с данными steam market.
    :param steam_resample: Период за который мы ищем среднюю стоимость предмета на steam market.
    :return: Список цен в йенах и количество проданных предметов.
    '''

    data = json.loads(data)

    if len(data) >= steam_resample:
        data = data[-1:-steam_resample-1:-1]

    price_list, sell_list = [], []

    c = CurrencyConverter()

    for item in data:
        price_list.append(round((c.convert(item[1], 'USD', 'CNY')), 2))
        sell_list.append(int(item[2]))

    return price_list, sell_list
