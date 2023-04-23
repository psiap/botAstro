from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.start import anti_flood
from keyboards.default.start_menu import buy_subs, buy_subs_frend
from loader import dp




@dp.message_handler(text=["❓ Поддержка"],state='*')
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    captions = """<b>🔧 Команда поддержки 🔧</b>

👋 Привет! Мы - команда поддержки, всегда готовы помочь Вам! Независимо от того, с чем у Вас возникли вопросы или проблемы, мы всегда готовы предложить Вам решения.

<b>📞 Для связи с нами, пожалуйста, воспользуйтесь следующими контактами:</b> 
Телеграм: 📲 @connecttoadmin

⏰ Мы работаем 7 дней в неделю, чтобы обеспечить Вам оперативную и качественную поддержку. Не стесняйтесь обращаться к нам в любое время - мы рады Вам помочь!

💼 Мы заботимся о Вас и Вашем опыте использования наших услуг. Благодарим за Ваше доверие и выбор нас!

    """
    await message.answer(captions)