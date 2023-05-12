from data.redis import (
    PRICE_THRESHOLD_KEY,
    BUFF_PERCENT_THRESHOLD_KEY,
    STEAM_PERCENT_THRESHOLD_KEY,
    STEAM_RESAMPLE_KEY,
    START_PARSE_KEY
)

from data.messages import START_COMMAND_MESSAGE

from functions import keyboards_clear

from loader import dp, bot

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start'], state='*')
async def start_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    await keyboards_clear(user_id=user_id, state=state)

    async with state.proxy() as data:
        if data:
            data.clear()
        data[PRICE_THRESHOLD_KEY] = 0.0
        data[BUFF_PERCENT_THRESHOLD_KEY] = 0.0
        data[STEAM_PERCENT_THRESHOLD_KEY] = 0.0
        data[STEAM_RESAMPLE_KEY] = 7
        data[START_PARSE_KEY] = False

    await bot.send_message(chat_id=user_id, text=START_COMMAND_MESSAGE)
