import datetime
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile, ContentTypes, CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from data.captcha import Captcha
from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_back, in_menu_get_floor, in_menu_set_info_users
from loader import dp, bot, PAYMENTS_PROVIDER_TOKEN
from utils.db_api.db import BotDB


@dp.callback_query_handler(lambda c: c.data.startswith('edit'))
async def buy_subs_users(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(call.from_user.id, f"Введите ваше имя")

    await state.set_state('start_name_1')

@dp.message_handler(text='Получить прогноз', state='*')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id, f"Введите ваше имя")

    await state.set_state('start_name_1')

@dp.message_handler(state='start_name_1')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Выберите ваш пол",reply_markup=await in_menu_get_floor())

    await state.set_state('start_name_2')

@dp.callback_query_handler(lambda c: c.data.startswith('floor'),state='start_name_2')
async def back_menu_callback(call: CallbackQuery, state: FSMContext):
    __userid = call.from_user.id
    answer_user = call.data.split(' ')[-1]
    if 'gotovo' in answer_user and '|' in answer_user:
        await call.message.edit_text(text=f'Введите место рождения')
        await state.update_data(floor=call.data.split("|")[-1])
        await state.set_state('start_country_3')
    else:
        await call.message.edit_text(text='Выберите ваш пол', reply_markup=await in_menu_get_floor(answer_user))


@dp.message_handler(state='start_country_3')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.update_data(country=message.text)
    await bot.send_message(message.from_user.id, text='Введите дату своего рождения',
                           reply_markup=await SimpleCalendar().start_calendar(), disable_web_page_preview=True)

    await state.set_state('start_date_4')


@dp.callback_query_handler(simple_cal_callback.filter(),state='start_date_4')
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict, state: FSMContext):
    selected, date = await SimpleCalendar().process_selection(callback_query, callback_data)
    await state.update_data(date_day=f'{date.strftime("%Y-%m-%d")}')
    await bot.send_message(callback_query.from_user.id,f"Выберите время вашего рождения")
    await state.set_state('start_date_5')

@dp.message_handler(state='start_date_5')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.update_data(date_hour=message.text)
    data = await state.get_data()
    await message.answer(f'Всё готово для создания вашей натальной карты, проверьте данные'
                         f'прежде чем отправлять их в наш чудесный астросервер\n\n'
                         f'{data["name"]}\n'
                         f'{data["floor"]}\n'
                         f'{data["country"]}\n'
                         f'{data["date_day"]}\n'
                         f'{data["date_hour"]}\n',reply_markup= await in_menu_set_info_users())
    await state.set_state('start_get_info_users_6')

