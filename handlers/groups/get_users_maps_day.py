import os
import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from datetime import datetime

from aiogram.types import InputFile

from handlers.users.start import anti_flood
from keyboards.default.start_menu import buy_subs, buy_subs_frend
from loader import dp, bot
from utils.db_api.db import BotDB


@dp.message_handler(text='📜 Карта дня',state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()

    get_db_telegram = BotDB()
    result = get_db_telegram.get_users(message.from_user.id)

    today = datetime.today().strftime('%Y-%m-%d')
    folder_path = 'data/images'

    # Создаем список всех файлов в папке
    files = os.listdir(folder_path)

    # Создаем список файлов с расширениями, соответствующими изображениям
    image_files = [file for file in files if file.endswith(('jpeg', 'png', 'bmp', 'gif', 'jpg'))]

    # Выбираем случайное изображение из списка
    random_image = random.choice(image_files)

    # Получаем сегодняшнюю дату в заданном формате

    today_save_bd = f"{today} {image_files.index(random_image)}"

    # edit_users_count_img(self,user_id,count_img)
    if result['count_img'] == None:
        image_path = f"{folder_path}/" + image_files[image_files.index(random_image)]
        photo = InputFile(image_path)
        await bot.send_photo(chat_id=message.chat.id, photo=photo)
        get_db_telegram.edit_users_count_img(message.from_user.id, today_save_bd)
    else:
        if result['count_img'].split(' ')[0] == today:
            image_path = f"{folder_path}/" + image_files[int(result['count_img'].split(' ')[-1])]
            photo = InputFile(image_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        else:
            image_path = f"{folder_path}/" +  image_files[image_files.index(random_image)]
            photo = InputFile(image_path)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
            get_db_telegram.edit_users_count_img(message.from_user.id, today_save_bd)

    captions = """🎴Карта дня - это изображение, которое отражает подсознательный настрой.  

Сконцентрируйтесь на карте и постарайтесь глубоко осмыслить то, что видите. Используйте метод ассоциаций, чтобы получить подсказку подсознания 🧩"""
    await message.answer(captions)