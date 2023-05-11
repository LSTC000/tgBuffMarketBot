import time

from parsers import buff_parser


def main():
    while True:
        buff_parser(price_threshold=50, percent_threshold=10, steam_resample='last_week')
        time.sleep(5)


if __name__ == '__main__':
    main()
