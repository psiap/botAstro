from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Данные рождения"),
            KeyboardButton(text="🌟 Подписка"),
            KeyboardButton(text="🔮 Прогноз"),
        ],
        [
            KeyboardButton(text="📜 Карта дня"),
            KeyboardButton(text="💫 Сны"),
            KeyboardButton(text="🤔 О боте"),
        ],
        [
            KeyboardButton(text="🌓 Общий прогноз"),
        ],
        [
            KeyboardButton(text="🪄 Подарить другу"),
            KeyboardButton(text="🚀 Смена города"),
        ],
        [
            KeyboardButton(text="❓ Поддержка"),
        ],
    ],
    resize_keyboard=True
)


buy_subs = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1 месяц'),
            KeyboardButton(text='3 месяца'),
            KeyboardButton(text='6 месяцев'),
        ],
        [
            KeyboardButton(text='1 год'),
        ],
        [
            KeyboardButton(text='Вернуться в главное меню'),
        ],
    ],
    resize_keyboard=True
)

buy_subs_frend = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1 месяц другу'),
            KeyboardButton(text='3 месяца другу'),

        ],
        [
            KeyboardButton(text='6 месяцев другу'),
            KeyboardButton(text='1 год другу'),
        ],
        [
            KeyboardButton(text='Вернуться в главное меню'),
        ],
    ],
    resize_keyboard=True
)

menu_personal_area = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Вернуться в главное меню'),
        ],
    ],
    resize_keyboard=True
)