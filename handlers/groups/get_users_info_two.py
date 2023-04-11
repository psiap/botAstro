import datetime
import time
from aiogram.types import InputFile, ContentTypes, CallbackQuery, ContentType
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
from utils.random_text import user_prog, get_img


@dp.callback_query_handler(lambda c: c.data.startswith('nice'), state='start_get_info_users_6')
async def buy_subs_users(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(text="""Чтобы я мог дать тебе точные советы на основе астрологических данных, отправь СВОЕ ТЕКУЩЕЕ местоположение. Если задумаешь переехать или улететь отдохнуть, в дальнейшем выбери кнопку ( )
Чтобы отправить геопозицию, нажми на иконку "скрепка" в поле ввода сообщения и выбери опцию "Отправить геопозицию". 🚀
""")

    await state.set_state('start_get_country_7')


@dp.message_handler(content_types=ContentType.ANY,state='start_get_country_7')
async def buy_subs_users(message: types.Message, state: FSMContext):
    try:
        location = message.location
        latitude = location.latitude
        longitude = location.longitude
        await state.update_data(country_two=f"{latitude} {longitude}")
    except Exception as E:
        await message.answer('Повторите попытку')
        return
    await message.answer("""Спасибо за предоставление необходимых данных! Я успешно составил твою натальную карту, которая является астрологическим паспортом 🪐
Теперь, чтобы получить персональный прогноз на определенный период времени, выбери день или период, который тебя интересует. 😊
Я с удовольствием помогу тебе раскрыть все тайны твоей судьбы и дам советы, как добиться успеха и счастья в жизни. 💫
Просто напиши мне, какой период тебя интересует, и я подготовлю для тебя подробный гороскоп. 📝
""",
                         reply_markup= await in_menu_set_date_prognos())

    await state.set_state('start_get_8')

def validate(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%d.%m.%Y").strftime('%d.%m.%Y'):
            return False
        return True
    except ValueError:
        return False
@dp.message_handler(state='start_get_temp')
async def buy_subs_users(message: types.Message, state: FSMContext):
    answer = message.text
    if validate(answer):

        await state.update_data(when_forecast=message.text)
        data = await state.get_data()
        get_db_telegram = BotDB()
        get_db_telegram.add_user_info_natal(user_id=message.from_user.id, name=data["name"], floor=data["floor"],
                                            place_of_birth=data["country"], date_of_birth=data["date_day"],
                                            time_of_birth=data["date_hour"], city_now=data["country_two"],
                                            when_forecast=data["when_forecast"])
        get_db_telegram.edit_forecast_users(message.from_user.id, answer)
        await message.answer(text=user_prog(message.text, message.from_user.id))
        await state.finish()
    else:
        await message.answer('Повторите попытку')

@dp.callback_query_handler(lambda c: c.data.startswith('dproc'), state='start_get_8')
async def buy_subs_users(call: CallbackQuery, state: FSMContext):
    answer_user = call.data.split(' ')[-1]
    if answer_user == 'get':
        await call.message.edit_text(text="📅 Укажите дату формате 01.01.2023")
        await state.set_state('start_get_temp')
    else:

        await state.update_data(when_forecast=call.data)
        data = await state.get_data()
        get_db_telegram = BotDB()
        get_db_telegram.add_user_info_natal(user_id=call.from_user.id,name=data["name"],floor=data["floor"],
                                            place_of_birth=data["country"],date_of_birth=data["date_day"],
                                            time_of_birth=data["date_hour"],city_now=data["country_two"],
                                            when_forecast=data["when_forecast"])
        get_db_telegram.edit_forecast_users(call.from_user.id, answer_user)
        if answer_user == 'today':
            date_now = datetime.datetime.now().strftime("%Y.%m.%d %H:%M").split(' ')[0]
        elif answer_user == 'tomorrow':
            prog_str = datetime.datetime.now() + datetime.timedelta(days=1)
            date_now = prog_str.strftime("%Y.%m.%d %H:%M").split(' ')[0]
        else:
            date_now = datetime.datetime.now().strftime("%d-%m-%Y")
        photo = InputFile(get_img(date_now=date_now))
        await bot.send_photo(call.from_user.id, photo=photo)
        await bot.send_message(call.from_user.id, text=user_prog(answer_user, call.from_user.id))
        #await call.message.edit_text(text=user_prog(answer_user, call.from_user.id))
        await state.finish()
#@dp.message_handler(state='start_get_8')
#async def buy_subs_users(message: types.Message, state: FSMContext):
#    await message.answer('Пока всё',
#                         reply_markup=menu_start)
#    await state.finish()