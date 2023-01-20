from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

menu_start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📁 Забронировать"),
            KeyboardButton(text="📅  Календарь"),
        ],
    ],
    resize_keyboard=True
)