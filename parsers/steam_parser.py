import re

from typing import Union

from data.config import HEADERS

from utils import steam_data_prepare

import requests

import numpy as np


def steam_parser(steam_market_url: str, steam_resample: str) -> Union[float, None]:
    '''
    :param steam_market_url: Ссылка на предмет в steam market.
    :param steam_resample: Метод группировки в steam market: 'all_time', 'last_week', 'last_month'.
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
        len_data = len(data)

        if steam_resample == 'last_week' and len_data >= 7:
            data = data[-1:-8:-1]
        if steam_resample == 'last_month' and len_data >= 30:
            data = data[-1:-31:-1]

        return data.mean()
    except Exception as ex:
        print(ex)
        return None
