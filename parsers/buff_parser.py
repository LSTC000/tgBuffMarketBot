from typing import Union

from data.config import HEADERS

from data.urls import BUFF_MARKET_JSON_URL, BUFF_GOODS_URL, BUFF_ITEM_JSON_URL

from parsers.steam_parser import steam_parser
from parsers.bargain_parser import bargain_parser

from utils import create_good_report

from loader import bot, items_cache

import httpx

from aiogram.dispatcher.storage import FSMContext
from data.redis import START_PARSE_REDIS_KEY


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
            if not data[START_PARSE_REDIS_KEY]:
                return True

        try:
            item_id = item.get('id')
            if user_id in items_cache.keys():
                if item_id in items_cache[user_id].keys() and items_cache[user_id][item_id] == item:
                    continue
                else:
                    items_cache[user_id][item_id] = item
            else:
                items_cache[user_id] = {}
                items_cache[user_id][item_id] = item

            steam_market_url = item.get('steam_market_url')

            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url=BUFF_ITEM_JSON_URL.format(item_id),
                        headers=HEADERS,
                        params={'chat_id': user_id}
                    )
                    response.raise_for_status()
                item_data = response.json()
                item_data = item_data.get('data')
            except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
                continue

            goods_infos = item_data.get('goods_infos').get(str(item_id))
            item = item_data.get('items')[0]

            steam_price_cny = float(goods_infos.get('steam_price_cny'))
            if steam_price_cny < price_threshold:
                continue

            sell_min_price = float(item.get('price'))
            if sell_min_price > steam_price_cny - (steam_price_cny * buff_percent_threshold / 100):
                continue

            steam_market_mean_price, steam_market_count_sell = await steam_parser(
                user_id=user_id,
                steam_market_url=steam_market_url,
                steam_resample=steam_resample
            )

            if steam_market_mean_price is None:
                continue
            if sell_min_price > steam_market_mean_price - (steam_market_mean_price * steam_percent_threshold / 100):
                continue

            paint_wear = item.get('asset_info').get('paintwear')
            if paint_wear:
                paint_wear = float(paint_wear)
            else:
                paint_wear = 0

            icon_url, icon_check = goods_infos.get('icon_url'), True
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(url=icon_url, headers=HEADERS, params={'chat_id': user_id})
                    response.raise_for_status()
            except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
                icon_check = False

            buff_good_url = BUFF_GOODS_URL.format(item_id)
            lowest_bargain_price = await bargain_parser(user_id=user_id, item=item)

            good_report = create_good_report(
                    good_name=goods_infos.get('name'),
                    paint_wear=paint_wear,
                    steam_market_mean_price=steam_market_mean_price,
                    steam_market_count_sell=steam_market_count_sell,
                    sell_min_price=sell_min_price,
                    buff_good_url=buff_good_url,
                    lowest_bargain_price=lowest_bargain_price
                )

            if icon_check:
                await bot.send_photo(chat_id=user_id, photo=response.content, caption=good_report)
            else:
                await bot.send_message(chat_id=user_id, text=good_report)
        except (AttributeError, KeyError):
            pass

    return None
