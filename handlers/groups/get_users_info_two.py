import datetime
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile, ContentTypes, CallbackQuery
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from data.captcha import Captcha
from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_back, in_menu_get_floor, in_menu_set_info_users, in_menu_set_date_prognos
from loader import dp, bot, PAYMENTS_PROVIDER_TOKEN
from utils.db_api.db import BotDB

@dp.callback_query_handler(lambda c: c.data.startswith('nice'), state='start_get_info_users_6')
async def buy_subs_users(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'Введите название города\n'
                                      f'(населённого пункта, В котором вы будете находиться в '
                                      f'находиться в период на который заказан прогноз)')

    await state.set_state('start_get_country_7')


@dp.message_handler(state='start_get_country_7')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.update_data(country_two=message.text)
    await message.answer('Ваша натальная карта составлена, для получения прогноза выберите день или период',
                         reply_markup= await in_menu_set_date_prognos())

    await state.set_state('start_get_8')

@dp.message_handler(state='start_get_8')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await message.answer('Пока всё',
                         reply_markup=menu_start)
    await state.finish()