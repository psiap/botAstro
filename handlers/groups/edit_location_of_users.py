import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from loader import dp
from utils.db_api.db import BotDB
from aiogram.types import InputFile, ContentTypes, CallbackQuery, ContentType

@dp.message_handler(text=['🚀 Смена города'],state='*')
@dp.throttled(anti_flood,rate=3)
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("""Вы переехали и сейчас у вас изменился город, хотел бы узнать, в каком вы сейчас городе 🌟\n
    Чтобы отправить геопозицию, нажми на иконку "скрепка" в поле ввода сообщения и выбери опцию "Отправить геопозицию". 🚀""")
    await state.set_state('edit_location')

@dp.message_handler(content_types=ContentType.ANY,state='edit_location')
async def start(message: types.Message, state: FSMContext):
    try:
        location = message.location
        latitude = location.latitude
        longitude = location.longitude
        get_db_telegram = BotDB()

        get_db_telegram.edit_location_from_user(message.from_user.id, f"{latitude} {longitude}")
        await message.answer(f"🔮 Отлично ваш {latitude} {longitude} бы отредактирован, теперь вы можете получить "
                             f"точную натальную карту")
        await state.finish()
    except Exception as e:
        await message.answer(f"Повторите попытку")