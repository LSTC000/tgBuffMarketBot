from fake_useragent import UserAgent


ua = UserAgent()
HEADERS = {
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': ua.random
}

BUFF_SLEEP_TIME = 3
