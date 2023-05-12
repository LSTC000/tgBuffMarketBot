import re

from typing import Union

from data.config import HEADERS

from utils import steam_data_prepare

import httpx

import numpy as np


async def steam_parser(user_id: int, steam_market_url: str, steam_resample: int) -> Union[float, None]:
    '''
    :param user_id: Телеграм user id.
    :param steam_market_url: Ссылка на предмет в steam market.
    :param steam_resample: Период за который мы ищем среднюю стоимость предмета на steam market.
    :return: Средняя цена предмета в steam market за указанный период (steam_resample). В случае ошибки - None.
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=steam_market_url, headers=HEADERS, params={'chat_id': user_id})
            response.raise_for_status()
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return None

    try:
        m = re.search(r'var line1=(.+);', response.text)
        data = np.array(steam_data_prepare(m.group(1)))

        if len(data) >= steam_resample:
            data = data[-1:-steam_resample-1:-1]

        return data.mean()
    except AttributeError:
        return None
