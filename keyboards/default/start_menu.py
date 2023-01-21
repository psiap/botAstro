from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Оплатить подписку"),
            KeyboardButton(text="Получить прогноз"),
        ],
        [
            KeyboardButton(text="Узнать больше про бота"),
        ],
    ],
    resize_keyboard=True
)


