from fake_useragent import UserAgent


ua = UserAgent()
HEADERS = {
    'User-Agent': ua.random
}

BUFF_SLEEP_TIME = 3
