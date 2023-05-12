from data.config import ROW_WIDTH

from data.callbacks import (
    CHANGE_PRICE_THRESHOLD_DATA,
    CHANGE_BUFF_PERCENT_THRESHOLD_DATA,
    CHANGE_STEAM_PERCENT_THRESHOLD_DATA,
    CHANGE_STEAM_RESAMPLE_DATA
)

from data.messages import (
    CHANGE_PRICE_THRESHOLD_IKB_MESSAGE,
    CHANGE_BUFF_PERCENT_THRESHOLD_IKB_MESSAGE,
    CHANGE_STEAM_PERCENT_THRESHOLD_IKB_MESSAGE,
    CHANGE_STEAM_RESAMPLE_IKB_MESSAGE
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def change_settings_ikb() -> InlineKeyboardMarkup:
    """
    :return: Клавиатура для изменения настроек.
    """

    ikb = InlineKeyboardMarkup(row_width=ROW_WIDTH)

    ikb.row(InlineKeyboardButton(
        text=CHANGE_PRICE_THRESHOLD_IKB_MESSAGE,
        callback_data=CHANGE_PRICE_THRESHOLD_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CHANGE_BUFF_PERCENT_THRESHOLD_IKB_MESSAGE,
        callback_data=CHANGE_BUFF_PERCENT_THRESHOLD_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CHANGE_STEAM_PERCENT_THRESHOLD_IKB_MESSAGE,
        callback_data=CHANGE_STEAM_PERCENT_THRESHOLD_DATA)
    )
    ikb.row(InlineKeyboardButton(
        text=CHANGE_STEAM_RESAMPLE_IKB_MESSAGE,
        callback_data=CHANGE_STEAM_RESAMPLE_DATA)
    )

    return ikb