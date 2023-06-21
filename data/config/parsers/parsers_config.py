import os

from fake_useragent import UserAgent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

ua = UserAgent()


STEAM_HEADERS = {
    'User-Agent': ua.random
}
BUFF_HEADERS = {
    'headers': 'your headers',
}
BUFF_COOKIES = {
    'cookies': 'your cookies',
}

PROXIES = os.getenv('PROXIES').split(',')
PROXY_LOGIN = os.getenv('PROXY_LOGIN')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')

BUFF_SLEEP_TIME = 3
STEAM_SLEEP_TIME = 0.1
