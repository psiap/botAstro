from datetime import timedelta, datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.users.start import anti_flood
from keyboards.default.start_menu import buy_subs, buy_subs_frend
from keyboards.inline.in_menu import in_menu_set_date_prognos_channel
from loader import dp, bot
from utils.moon_days_get import get_lunar_date


@dp.message_handler(text=['💫 Сны'],state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    with open('data/moon.csv','r+',encoding='utf-8') as file:
        data = [i.rstrip() for i in file.readlines()]

    date_now = datetime.now() + timedelta(days=1)
    await message.answer(data[get_lunar_date(date_now)[2]])



@dp.message_handler(text=["🌓 Общий прогноз"],state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    kb = await in_menu_set_date_prognos_channel()
    await message.answer('Выберите на когда',reply_markup=kb)


@dp.callback_query_handler(lambda c: c.data.startswith('pich'))
async def buy_subs_usersss(call: CallbackQuery, state: FSMContext):
    answer_user = call.data.split(' ')[-1]
    if answer_user == 'week':
        hashtag = '#week'
    else:
        hashtag = '#month'
    try:
        async for msg in bot.search_messages(chat_id=2141441, query=hashtag, limit=1):
            await bot.send_message(chat_id=call.from_user.id, text=msg.text)
    except Exception as e:
        await bot.send_message(chat_id=call.from_user.id, text="В данный момент прогноза нет")