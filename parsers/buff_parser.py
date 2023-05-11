from data.config import HEADERS

from data.urls import BUFF_MARKET_DATA_JSON_URL, BUFF_GOODS_URL

from parsers.steam_parser import steam_parser

import requests


def buff_parser(price_threshold: int, percent_threshold: int, steam_resample: str) -> None:
    '''
    :param price_threshold: Порог для оценки цены предмета.
    :param percent_threshold: Процентный порог для оценки фактической и наименьшей стоимости предмета.
    :param steam_resample: Метод группировки в steam market.
    :return: Пока ничего.
    '''

    try:
        response = requests.get(headers=HEADERS, url=BUFF_MARKET_DATA_JSON_URL)
        response.raise_for_status()
    except Exception as ex:
        print(ex)
        return

    data = response.json()

    try:
        items = data.get('data').get('items')

        for item in items:
            steam_price_cny = float(item.get('goods_info').get('steam_price_cny'))
            if steam_price_cny < price_threshold:
                continue

            sell_reference_price = float(item.get('sell_reference_price'))
            if sell_reference_price > steam_price_cny - (steam_price_cny * percent_threshold / 100):
                continue

            steam_market_url = item.get('steam_market_url')

            steam_market_mean_price = steam_parser(steam_market_url=steam_market_url, steam_resample=steam_resample)
            if steam_market_mean_price is None:
                continue
            if steam_market_mean_price < sell_reference_price:
                continue

            buff_goods_url = BUFF_GOODS_URL.format(item.get('id'))

            print(f'Buff price: {steam_price_cny}\nBuff reference price: {sell_reference_price}\n'
                  f'Steam market mean price: {steam_market_mean_price}\nBuff goods url: {buff_goods_url}\n'
                  f'Steam market url: {steam_market_url}')
    except Exception as ex:
        print(ex)
        return
