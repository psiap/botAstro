from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from loader import dp, bot, PAYMENTS_PROVIDER_TOKEN


@dp.message_handler(text='Оплатить подписку', state='*')
async def buy_subs_users(message: types.Message, state: FSMContext):
    __summ_add = 100
    __userid = message.from_user.id

    __summ_add = __summ_add * 100
    PRICE = types.LabeledPrice(label='Подписка', amount=__summ_add)
    await bot.send_invoice(message.chat.id, title='Оформление подписки',
                           description='Это твоя лучшая инвестиция',
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


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.pre_checkout_query_handler(lambda query: True, state='*')
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT,state='*')
async def got_payment(message: types.Message, state: FSMContext):
    __userid = message.chat.id
    add_balance = int(message.successful_payment.total_amount / 100)
    await message.answer(f"Подписка оплачена {add_balance}")
