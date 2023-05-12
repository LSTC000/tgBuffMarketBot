import time

from parsers import buff_parser


def main():
    while True:
        buff_parser(
            price_threshold=50,
            buff_percent_threshold=10,
            steam_percent_threshold=10,
            steam_resample=7
        )
        time.sleep(5)


if __name__ == '__main__':
    main()
