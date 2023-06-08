import re

from data.config import STEAM_HEADERS

from utils import steam_data_prepare

import httpx


async def steam_parser(user_id: int, steam_market_url: str, steam_resample: int) -> tuple:
    '''
    :param user_id: Телеграм user id.
    :param steam_market_url: Ссылка на предмет в steam market.
    :param steam_resample: Период за который мы ищем среднюю стоимость предмета на steam market.
    :return: Средняя цена предмета в steam market за указанный период (steam_resample) и количество проданных предметов.
        В случае ошибки - None.
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=steam_market_url, headers=STEAM_HEADERS, params={'chat_id': user_id})
            response.raise_for_status()
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return None, None

    try:
        m = re.search(r'var line1=(.+);', response.text)
        data_price, data_sell = steam_data_prepare(data=m.group(1), steam_resample=steam_resample)

        data_price_mean = round(sum(data_price) / len(data_price), 2)
        data_price_threshold = data_price_mean + (data_price_mean * 0.2)
        new_data_price = []

        for price in data_price:
            if price <= data_price_threshold:
                new_data_price.append(price)

        return round(sum(new_data_price) / len(new_data_price), 2), sum(data_sell)
    except AttributeError:
        return None, None
