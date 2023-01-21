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


@dp.message_handler(CommandStart(),state='*')
@dp.throttled(anti_flood,rate=3)
async def start(message: types.Message, state: FSMContext):
    await state.finish()

    await state.finish()
    photo = InputFile("data/1.jpg")
    msg = await bot.send_photo(chat_id=message.from_user.id, photo=photo,caption="<b>Добро пожаловать!</b>\n\n"
                         "<b>Астроло́гия</b> — группа описательных и предсказательных практик, традиций и "
                                                                           "верований, постулирующи"
                                                                           "х воздействие небесных тел"
                                                                           " на земной мир и человека\n\n",
                         reply_markup=menu_start)


       # caption=message.caption,
    #    reply_markup=await in_menu_back(),
   # )