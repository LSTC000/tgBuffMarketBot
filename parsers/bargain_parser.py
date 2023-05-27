from typing import Union

from data.config import HEADERS

from data.urls import BUFF_ITEM_JSON_URL

import httpx


async def bargain_parser(user_id: int, item_id: str) -> Union[float, None]:
    '''
    :param user_id: Телеграм user id.
    :param item_id: id предмета в Buff.
    :return: Минимальная цена предмета для торга, если он возможен. Иначе - None.
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=BUFF_ITEM_JSON_URL.format(item_id),
                headers=HEADERS,
                params={'chat_id': user_id}
            )
            response.raise_for_status()
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return None

    try:
        data = response.json()
        item = data.get('data').get('items')[0]
        item_info = item.get('asset_info').get('info')

        if 'inspect_state' in item_info.keys():
            return float(item.get('lowest_bargain_price'))
        else:
            return None
    except (AttributeError, KeyError):
        return None
