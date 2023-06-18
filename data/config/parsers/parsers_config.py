import os

from fake_useragent import UserAgent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ua = UserAgent()


STEAM_HEADERS = {
    'User-Agent': ua.random
}
BUFF_HEADERS = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Referer': 'https://buff.163.com/market/csgo',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 OPR/99.0.0.0',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Opera";v="99", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
BUFF_COOKIES = {
    'Device-Id': '6RCJfWbDswkX3D6LMc1D',
    'Locale-Supported': 'ru',
    'game': 'csgo',
    'NTES_YD_SESS': 'tXl83fbgj1zxdyXigEUcsJzHl9I1334WO2tQX_scEEHTQwT6Mg0_YXVjgZsGNSxOi0QByFegGHrS1l5GseizOPDXS_3OvzDPlrFrx_XMQwyhx312H7f8bh.1_WnhHYzHsRA0z1SslufjQ89ls4Jszgsr2pxm82xD8B48cP0drJJ286ZNQb5FAkVmHwG0MsUQycnwYCVcukI_3Evt70PpP92TWlcSg8Lv64CdR1FbOf3.b',
    'S_INFO': '1686228509|0|0&60##|7-9132170674',
    'P_INFO': '7-9132170674|1686228509|1|netease_buff|00&99|RU&1686065031&netease_buff#RU&null#10#0#0|&0|null|7-9132170674',
    'remember_me': 'U1105897071|dL7G7DBJESTYejGsxtjsF4iAmDrZyBFz',
    'session': '1-3OT2r1u8-YYeMsCJ2X2VpWbl1KaGX4BwWdEGKqye6EQ62032417079',
    'csrf_token': 'IjIyNTlhN2QxZjY0ZWUyOGE0ODM1MGRlOGNlMjA1Nzk0ODZhMmQyNzAi.F2NfuA.RPWoifQ4raK2zP5-Q8PB6pcMTTA'
}

PROXIES = os.getenv('PROXIES').split(',')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

BUFF_SLEEP_TIME = 3
STEAM_SLEEP_TIME = 0.1
