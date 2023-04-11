from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from keyboards.default.start_menu import buy_subs, buy_subs_frend
from loader import dp




@dp.message_handler(text='🪄 Подарить другу',state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите на сколько', reply_markup=buy_subs_frend)