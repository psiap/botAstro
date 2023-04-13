from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from loader import dp


@dp.message_handler(text='🤔 О боте',state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    captions = """🔮Ежедневный персональный гороскоп в твоем телеграмме!

Как это работает? 

📍При запуске бота необходимо ввести  время, место и дату вашего рождения. На их основе бот строит и анализирует натальную карту. По ней ежедневно создаются индивидуальные рекомендации! 

💯 Эти советы значительно точнее традиционных обобщённых гороскопов для знака зодиака, позволяют лучше планировать и эффективнее принимать решения, так как они рассчитаны для конкретного человека 🎯"""
    await message.answer(captions)