def create_goods_report(
    steam_price_cny: float,
    sell_min_price: float,
    steam_market_mean_price: float,
    steam_resample: int,
    buff_goods_url: str
) -> str:
    '''
    :param steam_price_cny: Оценочная стоимость.
    :param sell_min_price: Наименьшая доступная цена.
    :param steam_market_mean_price: Средняя цена за период steam_resample в steam market.
    :param steam_resample: Количество дней, за которое мы ищем среднюю стоимость предмета на steam market.
    :param buff_goods_url: Ссылка на предмет в Buff.
    :return: Строка с информацией о товаре.
    '''

    return f'<b>Оценочная стоимость:</b> {steam_price_cny}\n' \
           f'<b>Цена 1-го предмета:</b> {sell_min_price}\n' \
           f'<b>Цена в steam за {steam_resample} дней:</b> {steam_market_mean_price: .2f}\n\n' \
           f'{buff_goods_url}'
