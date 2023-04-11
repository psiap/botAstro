import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InputFile

from handlers.groups.get_users_info_two import validate
from keyboards.inline.in_menu import in_menu_set_date_prognos_forecast
from loader import dp, bot
from utils.db_api.db import BotDB
from utils.random_text import user_prog, get_img


@dp.message_handler(text=['🔮 Прогноз'],state='*')
async def start(message: types.Message, state: FSMContext):
    await message.answer("""Просто напиши мне, какой период тебя интересует, и я подготовлю для тебя подробный гороскоп. 📝
    """,
                         reply_markup=await in_menu_set_date_prognos_forecast())
#dforproc
    await state.set_state('start_forecast')


@dp.callback_query_handler(lambda c: c.data.startswith('dforproc'), state='start_forecast')
async def buy_subs_users(call: CallbackQuery, state: FSMContext):
    try:
        answer_user = call.data.split(' ')[-1]
        if answer_user == 'get':
            await call.message.edit_text(text="📅 Укажите дату формате 01.01.2023")
            await state.set_state('start_forecast_two_users')
        else:
            if answer_user == 'today':
                date_now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M").split(' ')[0]
            elif answer_user == 'tomorrow':
                prog_str = datetime.datetime.now() + datetime.timedelta(days=1)
                date_now = prog_str.strftime("%Y.%m.%d %H:%M").split(' ')[0]
            else:
                date_now = datetime.datetime.now().strftime("%d-%m-%Y")
            photo = InputFile(get_img(date_now=date_now))
            await bot.send_photo(call.from_user.id, photo=photo)
            await bot.send_message(call.from_user.id, text=user_prog(answer_user,call.from_user.id))
            #await call.message.edit_text(text=user_prog(answer_user,call.from_user.id))
            get_db_telegram = BotDB()
            get_db_telegram.edit_forecast_users(call.from_user.id, answer_user)
            await state.finish()
    except Exception as E:
        await call.message.edit_text(text="Укажите все данные и повторите попытку")
        await state.finish()


@dp.message_handler(state='start_forecast_two_users')
async def buy_subs_users(message: types.Message, state: FSMContext):
    try:
        answer = message.text
        if validate(answer):
            await message.answer(text=user_prog(message.text, message.from_user.id))
            get_db_telegram = BotDB()
            get_db_telegram.edit_forecast_users(message.from_user.id, answer)
            await state.finish()
        else:
            await message.answer('Повторите попытку')
    except Exception as E:
        await message.answer("Укажите все данные и повторите попытку")
        await state.finish()