from data.redis import START_PARSE_KEY

from loader import dp

from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.message_handler(commands=['stop_parse'], state='*')
async def stop_parse_command(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data[START_PARSE_KEY] = False
