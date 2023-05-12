from asyncio import sleep

from data.redis import (
    PRICE_THRESHOLD_KEY,
    BUFF_PERCENT_THRESHOLD_KEY,
    STEAM_PERCENT_THRESHOLD_KEY,
    STEAM_RESAMPLE_KEY,
    START_PARSE_KEY
)

from data.config import BUFF_SLEEP_TIME

from data.messages import START_PARSE_COMMAND_MESSAGE, STOP_PARSE_COMMAND_MESSAGE

from parsers import buff_parser

from loader import dp, bot

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['start_parse'], state='*')
async def start_parse_command(message: types.Message, state: FSMContext) -> None:
    user_id = message.from_user.id

    await bot.send_message(chat_id=user_id, text=START_PARSE_COMMAND_MESSAGE)

    async with state.proxy() as data:
        data[START_PARSE_KEY] = True

    while True:
        stop = await buff_parser(
            user_id=user_id,
            price_threshold=data[PRICE_THRESHOLD_KEY],
            buff_percent_threshold=data[BUFF_PERCENT_THRESHOLD_KEY],
            steam_percent_threshold=data[STEAM_PERCENT_THRESHOLD_KEY],
            steam_resample=data[STEAM_RESAMPLE_KEY],
            state=state
        )

        if stop is not None:
            await bot.send_message(chat_id=user_id, text=STOP_PARSE_COMMAND_MESSAGE)
            break

        await sleep(BUFF_SLEEP_TIME)