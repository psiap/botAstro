import datetime
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ContentTypes, CallbackQuery, ContentType
from aiogram_calendar import simple_cal_callback, SimpleCalendar

from data.captcha import Captcha
from handlers.groups.get_users_info_two import validate
from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_back, in_menu_get_floor, in_menu_set_info_users, \
    in_menu_set_info_users_time_created
from loader import dp, bot, PAYMENTS_PROVIDER_TOKEN
from utils.db_api.db import BotDB


@dp.callback_query_handler(lambda c: c.data.startswith('edit'),state='*')
async def buy_subs_users(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await bot.send_message(call.from_user.id, """<i>Привет</i>, <b>друг</b>! 😃\n
Я - астрологический бот, готовый помочь тебе раскрыть тайны вселенной! 🌟\n
Пожалуйста, скажи мне, как я могу называть тебя? 🤔\n
Просто напиши свое имя в ответном сообщении, и мы продолжим наше знакомство! 🚀""")

    await state.set_state('start_name_1')

@dp.message_handler(text="Данные рождения", state='*')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.finish()

    await bot.send_message(message.from_user.id, """<b>Пожалуйста, скажите мне, как вас зовут?🌟</b>

Просто напишите своё имя в ответном сообщении. Я начну создавать вашу натальную карту.🚀
    """)

    await state.set_state('start_name_1')

@dp.message_handler(state='start_name_1')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"""<b>Укажите ваш пол.🧘</b>
    
Пока наши рекомендации не деляться на мужчин и женщин, но в перспективе мы усовершенствуем гороскоп, поэтому собираем  эту <code>информацию</code>.🤔\n""",reply_markup=await in_menu_get_floor())

    await state.set_state('start_name_2')

@dp.callback_query_handler(lambda c: c.data.startswith('floor'),state='start_name_2')
async def back_menu_callback(call: CallbackQuery, state: FSMContext):
    __userid = call.from_user.id
    answer_user = call.data.split(' ')[-1]
    if 'gotovo' in answer_user and '|' in answer_user:
        await call.message.edit_text(text="""Укажите место своего рождения на карте, чтобы точность моих советов была ещё выше. Для этого используйте приложение Telegram на мобильном устройстве(в версии для ПК этого сделать пока нельзя).🚀
        
<b>Нажмите 📎“скрепку” справа от поля ввода сообщения,</b> выберите <code>“отправить геопозицию”</code> внизу. Перемещаясь по карте при помощи свайпов, выберите нужное место, можно ограничиться городом или другим населённым пунктом (если не можете указать точный адрес)
""")
        await state.update_data(floor=call.data.split("|")[-1])
        await state.set_state('start_country_3')
        with open('data/maps1.jpg', 'rb') as photo1, open('data/maps2.jpg', 'rb') as photo2:
            # Создаем список объектов InputMediaPhoto
            media = [types.InputMediaPhoto(photo1), types.InputMediaPhoto(photo2)]
            # Отправляем список объектов InputMediaPhoto в одном сообщении
            await bot.send_media_group(chat_id=call.from_user.id, media=media)
    else:
        await call.message.edit_text(text=f'📲 Теперь укажите ваш пол', reply_markup=await in_menu_get_floor(answer_user))



@dp.message_handler(content_types=ContentType.ANY,state='start_country_3')
async def buy_subs_users(message: types.Message, state: FSMContext):
    try:
        location = message.location
        latitude = location.latitude
        longitude = location.longitude
        await state.update_data(country=f"{latitude} {longitude}")
    except Exception as E:
        await message.answer('Повторите попытку')
        return
    await message.answer(f"""Ещё немного! <b>Мне нужно узнать дату вашего рождения. Просто напишите её в ответном сообщении в формате ДД.ММ.ГГГГ.🚀</b>
    
Например — <code>01.01.1990.</code> Это поможет мне определить расположения небесных тел в момент вашего рождения, что повысит точность моих рекомендаций! 🌟
""")
    await state.set_state('start_date_4')


@dp.message_handler(state='start_date_4')
async def buy_subs_users(message: types.Message, state: FSMContext):
    if validate(message.text):
        await state.update_data(date_day=f'{message.text}')
        await message.answer(f"""<b>Почти готово. Осталось узнать время, когда вы родились. </b>
        
Введите его в формате <code>ЧЧ:ММ (например, 05:25)</code> в ответном сообщении или выберите время приблизительно при помощи кнопок. 🌟 🚀
""",reply_markup=await in_menu_set_info_users_time_created())
        await state.set_state('start_date_5')
    else:
        await message.answer(f"📅 Повторите попытку")


def validate_time(date_text):
    try:
        if date_text != datetime.datetime.strptime(date_text, "%H:%M").strftime('%H:%M'):
            return False
        return True
    except ValueError:
        return False


@dp.callback_query_handler(lambda c: c.data.startswith('createdtime'),state='start_date_5')
async def back_menu_callback(call: CallbackQuery, state: FSMContext):
    answer_user = call.data.split(' ')[-1]
    await state.update_data(date_hour=answer_user)
    data = await state.get_data()
    await bot.send_message(call.from_user.id, f'Отлично. Всё готово для создания вашей натальной карты\n\n'
                                              f'🧾 Проверьте, всё ли верно, прежде чем отправлять информацию в наш чудесный астросервер\n\n'
                         f'1. {data["name"]}\n'
                         f'2. {data["floor"]}\n'
                         f'3. {data["country"]}\n'
                         f'4. {data["date_day"]}\n'
                         f'5. {data["date_hour"]}\n', reply_markup=await in_menu_set_info_users())

    await state.set_state('start_get_info_users_6')

@dp.message_handler(state='start_date_5')
async def buy_subs_users(message: types.Message, state: FSMContext):
    if validate_time(message.text):
        await state.update_data(date_hour=message.text)
        data = await state.get_data()
        await message.answer(f'Отлично. Всё готово для создания вашей натальной карты\n\n'
                            f'🧾 Проверьте, всё ли верно, прежде чем отправлять информацию в наш чудесный астросервер\n\n'
                             f'1. {data["name"]}\n'
                             f'2. {data["floor"]}\n'
                             f'3. {data["country"]}\n'
                             f'4. {data["date_day"]}\n'
                             f'5. {data["date_hour"]}\n',reply_markup= await in_menu_set_info_users())

        await state.set_state('start_get_info_users_6')
    else:
        await message.answer(f"📅 Повторите попытку")
