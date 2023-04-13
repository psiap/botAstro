import datetime
import time

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InputFile

from data.captcha import Captcha
from keyboards.default import menu_start
from keyboards.inline.in_menu import in_menu_back
from loader import dp, bot
from utils.db_api.db import BotDB
from utils.random_text import get_img


async def anti_flood(*args, **kwargs):
    message = args[0]
    if message.from_user.id not in Captcha.passed_captcha_users:
        captcha = Captcha()
        captcha.register_handlers(dp)

        await bot.send_message(
            message.chat.id,
            captcha.get_caption(),
            reply_markup=captcha.get_captcha_keyboard()
        )
        return



@dp.message_handler(text='🔙 Назад', state='*')
async def back(message: types.Message, state: FSMContext):
    await message.answer("", reply_markup=menu_start)
    await state.finish()

@dp.message_handler(text=['Вернуться в главное меню'],state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    photo = InputFile(get_img())
    msg = await bot.send_video(chat_id=message.from_user.id, video=open('data/video_2023-04-09_03-16-55 (online-video-cutter.com).mp4', 'rb'), caption="""Здравствуйте 👋 Рад, что вы решили использовать мои астрологические знания и опыт!

🔹Я создан, чтобы сделать вашу жизнь гармоничной и эффективной👌
🔹Я создаю астрологические рекомендации, которые помогают принимать верные решения и управлять своей судьбой.
🔹Я использую передовой алгоритм астрологического планирования, учитывающий точное положение планет в конкретный момент времени 🔭

Давайте работать вместе, чтобы не упускать возможности, поймать удачу 💰 и легче справляться с трудными моментами!
    """,
                               reply_markup=menu_start)



async def chech_users_frend_subs(message: types.Message):
    get_db_telegram = BotDB()
    users_id = message.text.split(' ')[-1]
    result = get_db_telegram.get_check_user_frends(user_id=users_id)
    if result:
        get_db_telegram.get_check_user_frends_delete(keyid=result['keyid'])
        datenowtilda = datetime.timedelta(days=int(result['daysubs']))
        date_now = datetime.datetime.now() + datenowtilda
        get_db_telegram.add_subs_users(message.from_user.id, date_now)
        await message.answer(f"Отлично, вам подарили подписку на бота, она действует до {date_now}")




@dp.message_handler(CommandStart(),state='*')
async def start(message: types.Message, state: FSMContext):
    if ' ' in message.text:
        await chech_users_frend_subs(message=message)
    await state.finish()

    get_db_telegram = BotDB()
    user_id, username, date_register = message.from_user.id, message.from_user.username, datetime.datetime.now()
    get_db_telegram.get_start_check_user(user_id, username, date_register)

    #photo = InputFile(get_img())

    msg = await bot.send_video(message.from_user.id, video=open('data/video_2023-04-09_03-16-55 (online-video-cutter.com).mp4', 'rb'),caption="""Здравствуйте 👋 Рад, что вы решили использовать мои астрологические знания и опыт!

🔹Я создан, чтобы сделать вашу жизнь гармоничной и эффективной👌
🔹Я создаю астрологические рекомендации, которые помогают принимать верные решения и управлять своей судьбой.
🔹Я использую передовой алгоритм астрологического планирования, учитывающий точное положение планет в конкретный момент времени 🔭

Давайте работать вместе, чтобы не упускать возможности, поймать удачу 💰 и легче справляться с трудными моментами!
    """,
                         reply_markup=menu_start)


