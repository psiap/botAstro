from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from loader import dp


@dp.message_handler(text='🤔 О боте',state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    captions = """<b>🔮Ежедневный персональный гороскоп в Вашем телеграмме!</b>

Как это работает? 

<b>📍При запуске бота необходимо ввести  время, место и дату Вашего рождения.</b> На их основе бот строит и анализирует натальную карту. По ней ежедневно создаются индивидуальные рекомендации! 

💯 Эти советы значительно точнее традиционных обобщённых гороскопов для знака зодиака, <b>позволяют лучше планировать и эффективнее принимать решения, так как они рассчитаны для конкретного человека 🎯</b>
"""
    await message.answer(captions)