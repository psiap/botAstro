import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from keyboards.default.start_menu import buy_subs, menu_personal_area
from loader import dp, bot, PAYMENTS_PROVIDER_TOKEN
from utils.db_api.db import BotDB


@dp.message_handler(text='🌟 Подписка', state='*')
async def buy_subs_users(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Выберите длительность оплачиваемого периода⏱',reply_markup=buy_subs)

@dp.message_handler(text=['1 месяц', '3 месяца', '6 месяцев', '1 год'],state='*')
async def add_balance_incek(message: types.Message, state: FSMContext):
    __userid = message.from_user.id
    __message_text_user = message.text
    if __message_text_user == '1 месяц':
        __summ_add = 300
    elif __message_text_user == '3 месяца':
        __summ_add = 800
    elif __message_text_user == '6 месяцев':
        __summ_add = 1500
    elif __message_text_user == '1 год':
        __summ_add = 2900
    else:
        await message.answer(f"Повторите попытку",
                             reply_markup=menu_personal_area)
        await state.set_state('personal')
        return
    await state.set_state('by_subs')
    __summ_add = __summ_add * 100
    PRICE = types.LabeledPrice(label='Подписка', amount=__summ_add)
    await bot.send_invoice(message.chat.id, title='Оформление подписки',
                           description='Это Ваша лучшая инвестиция 👌',
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',
                           photo_url='https://www.simplybuzzes.com/wp-content/uploads/2020/02/numerology-1-1080x600.jpg',
                           photo_height=608,  # !=0/None or picture won't be shown
                           photo_width=1081,
                           photo_size=512,
                           is_flexible=False,  # True If you need to set up Shipping Fee
                           prices=[PRICE],
                           start_parameter='time-machine-example',
                           payload='HAPPY FRIDAYS COUPON')




@dp.pre_checkout_query_handler(lambda query: True,state='by_subs')
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.pre_checkout_query_handler(lambda query: True, state='by_subs')
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT,state='by_subs')
async def got_payment(message: types.Message, state: FSMContext):
    __userid = message.chat.id
    add_balance = int(message.successful_payment.total_amount / 100)


    if add_balance == 300:
        datenowtilda = datetime.timedelta(days=31)
    elif add_balance == 800:
        datenowtilda = datetime.timedelta(days=92)
    elif add_balance == 1500:
        datenowtilda = datetime.timedelta(days=180)
    elif add_balance == 2900:
        datenowtilda = datetime.timedelta(days=365)
    else:
        datenowtilda = datetime.timedelta(days=1)

    date_now = datetime.datetime.now() + datenowtilda
    get_db_telegram = BotDB()
    get_db_telegram.add_subs_users(__userid, date_now)

    date_tranz = datetime.datetime.now()
    get_db_telegram.add_tranz_users(__userid,add_balance,date_tranz)

    await message.answer(f"Спасибо за покупку! ⌛ <b>Подписка активна</b> и действует до  {date_now}")
    await state.finish()

