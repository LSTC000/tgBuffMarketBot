import re

from typing import Union

from data.config import HEADERS

from utils import steam_data_prepare

import requests

import numpy as np


def steam_parser(steam_market_url: str, steam_resample: int) -> Union[float, None]:
    '''
    :param steam_market_url: Ссылка на предмет в steam market.
    :param steam_resample: Период за который мы ищем среднюю стоимость предмета на steam market.
    :return: Средняя цена предмета в steam market за указанный период (steam_resample). В случае ошибки - None.
    '''

    try:
        response = requests.get(headers=HEADERS, url=steam_market_url)
        response.raise_for_status()
    except Exception as ex:
        print(ex)
        return None

    try:
        m = re.search(r'var line1=(.+);', response.text)
        data = np.array(steam_data_prepare(m.group(1)))

        if len(data) >= steam_resample:
            data = data[-1:-steam_resample-1:-1]

        return data.mean()
    except Exception as ex:
        print(ex)
        return None
