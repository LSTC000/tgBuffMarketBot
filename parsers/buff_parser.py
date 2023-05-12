from data.config import HEADERS

from data.urls import BUFF_MARKET_JSON_URL, BUFF_GOODS_URL

from parsers.steam_parser import steam_parser

from loader import items_cache

import requests


def buff_parser(
    price_threshold: int,
    buff_percent_threshold: int,
    steam_percent_threshold: int,
    steam_resample: int
) -> None:
    '''
    :param price_threshold: Порог для оценки цены предмета.
    :param buff_percent_threshold: Процентный порог для оценки фактической и наименьшей стоимости предмета.
    :param steam_percent_threshold: Процентный порог для наименьшей и средней на steam market стоимости предмета.
    :param steam_resample: Количество дней, за которое мы ищем среднюю стоимость предмета на steam market.
    :return: Пока ничего.
    '''

    try:
        response = requests.get(headers=HEADERS, url=BUFF_MARKET_JSON_URL)
        response.raise_for_status()
    except Exception as ex:
        print(ex)
        return

    data = response.json()

    try:
        items = data.get('data').get('items')

        for item in items:
            item_id = item.get('id')
            if item_id in items_cache.keys():
                if items_cache[item_id] == item:
                    continue

            steam_price_cny = float(item.get('goods_info').get('steam_price_cny'))
            if steam_price_cny < price_threshold:
                continue

            sell_min_price = float(item.get('sell_min_price'))
            if sell_min_price > steam_price_cny - (steam_price_cny * buff_percent_threshold / 100):
                continue

            steam_market_url = item.get('steam_market_url')

            steam_market_mean_price = steam_parser(steam_market_url=steam_market_url, steam_resample=steam_resample)
            if steam_market_mean_price is None:
                continue
            if sell_min_price > steam_market_mean_price - (steam_market_mean_price * steam_percent_threshold / 100):
                continue

            buff_goods_url = BUFF_GOODS_URL.format(item_id)
            items_cache[item_id] = item

            print(f'Buff price: {steam_price_cny}\nBuff min price: {sell_min_price}\n'
                  f'Steam market mean price: {steam_market_mean_price}\nBuff goods url: {buff_goods_url}\n'
                  f'Steam market url: {steam_market_url}')
    except Exception as ex:
        print(ex)
        return
