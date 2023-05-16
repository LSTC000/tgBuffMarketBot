def create_good_report(
    good_name: str,
    steam_price_cny: float,
    sell_min_price: float,
    buff_good_url: str
) -> str:
    '''
    :param good_name: Название предмета.
    :param steam_price_cny: Ориентировочная стоимость.
    :param sell_min_price: Стоимость 1-го предмета для покупки.
    :param buff_good_url: Ссылка на предмет в Buff.
    :return: Строка с информацией о товаре.
    '''

    clear_steam_price_cny = steam_price_cny * 0.87

    return f'Предмет: <a href="{buff_good_url}">{good_name}</a>\n' \
           f'Цена покупки buff: {sell_min_price}Y\n' \
           f'Цена стим: {steam_price_cny}Y ({clear_steam_price_cny: .2f}Y)\n' \
           f'Профит ~ {((clear_steam_price_cny - sell_min_price) * 100) / sell_min_price: .2f}%'
