from typing import Union

from data.config import HEADERS

from data.urls import BUFF_MARKET_JSON_URL, BUFF_GOODS_URL

from parsers.steam_parser import steam_parser

from loader import bot, items_cache

import httpx

from aiogram.dispatcher.storage import FSMContext
from data.redis import START_PARSE_KEY


async def buff_parser(
    user_id: int,
    price_threshold: float,
    buff_percent_threshold: float,
    steam_percent_threshold: float,
    steam_resample: int,
    state: FSMContext
) -> Union[bool, None]:
    '''
    :param user_id: Телеграм user id.
    :param price_threshold: Порог для оценки цены предмета.
    :param buff_percent_threshold: Процентный порог для оценки фактической и наименьшей стоимости предмета.
    :param steam_percent_threshold: Процентный порог для наименьшей и средней на steam market стоимости предмета.
    :param steam_resample: Количество дней, за которое мы ищем среднюю стоимость предмета на steam market.
    :param state: FSMContext
    :return: True, если пользователь остановил парсер, иначе - None.
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=BUFF_MARKET_JSON_URL, headers=HEADERS, params={'chat_id': user_id})
            response.raise_for_status()
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return None

    try:
        data = response.json()
        items = data.get('data').get('items')
    except (AttributeError, KeyError):
        return None

    for item in items:
        async with state.proxy() as data:
            if not data[START_PARSE_KEY]:
                return True

        try:
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
            steam_market_mean_price = await steam_parser(
                user_id=user_id,
                steam_market_url=steam_market_url,
                steam_resample=steam_resample
            )
            if steam_market_mean_price is None:
                continue
            if sell_min_price > steam_market_mean_price - (steam_market_mean_price * steam_percent_threshold / 100):
                continue

            buff_goods_url = BUFF_GOODS_URL.format(item_id)
            items_cache[item_id] = item

            await bot.send_message(chat_id=user_id, text=buff_goods_url)
        except (AttributeError, KeyError):
            pass

    return None
