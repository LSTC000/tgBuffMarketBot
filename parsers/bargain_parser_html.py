from typing import Union

from data.config import HEADERS

from bs4 import BeautifulSoup

import httpx


async def bargain_parser_html(user_id: int, buff_good_url: str) -> Union[float, None]:
    '''
    :param user_id: Телеграм user id.
    :param buff_good_url: Ссылка на предмета в Buff.
    :return: Минимальная цена предмета для торга, если он возможен. Иначе - None.
    '''

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url=buff_good_url, headers=HEADERS, params={'chat_id': user_id})
            response.raise_for_status()
    except (httpx.HTTPError, httpx.RequestError, httpx.TimeoutException):
        return None

    try:
        soup = BeautifulSoup(response.text, 'lxml')

        div_detail_tab_cont = soup.find('div', _class='detail-tab-cont')
        table_list_tb = div_detail_tab_cont.find('table', _class='list_tb')
        tbody_list_tb_csgo = table_list_tb.find('tbody', _class='list_tb_csgo')
        tr_selling = tbody_list_tb_csgo.find('tr', _class='selling')
        td_t_Left = tr_selling.find_all('td', _class='t_Left')[-1]
        a_bargain = td_t_Left.find('a', _class='bargain')

        return float(a_bargain['data-lowest-bargain-price'])
    except (AttributeError, KeyError):
        return None
