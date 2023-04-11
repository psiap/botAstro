import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from loader import dp
from utils.db_api.db import BotDB


@dp.message_handler(text=['Бесплатная подписка'],state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    get_db_telegram = BotDB()
    result = get_db_telegram.get_check_user_free_version(message.from_user.id)
    if result:
        await message.answer(f"🔮 Попробуйте 3 дня PREMIUM. Далее 100 руб за 3 месяцев."
                             f"🧙 Получите консультацию у астрологов, будьте в курсе своей судьбы. "
                             f"Изучите совместимость партнёров и персональные гороскопы на каждый день!"
                             f"\n<b>Действия вашей подписки до </b> <code>{result}</code>")
    else:
        await message.answer(f"🔮 Извините вы уже использовали пробную версию")