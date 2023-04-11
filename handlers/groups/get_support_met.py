from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from keyboards.default.start_menu import buy_subs, buy_subs_frend
from loader import dp




@dp.message_handler(text=["❓ Поддержка"],state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    captions = """🔧 Команда поддержки 🔧

👋 Привет! Мы - команда поддержки, всегда готовы помочь вам! Независимо от того, с чем у вас возникли вопросы или проблемы, мы всегда готовы предложить вам решения.

📞 Для связи с нами, пожалуйста, воспользуйтесь следующими контактами:
Телеграм: 📲 @mariaastroclub

⏰ Мы работаем круглосуточно, 7 дней в неделю, чтобы обеспечить вам оперативную и качественную поддержку. Не стесняйтесь обращаться к нам в любое время - мы рады вам помочь!

💼 Мы заботимся о вас и вашем опыте использования наших услуг. Благодарим за ваше доверие и выбор нас!
    """
    await message.answer(captions)