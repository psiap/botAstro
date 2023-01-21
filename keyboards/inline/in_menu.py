import datetime

from aiogram import types

from data.config import ADMINS
from utils.db_api.db import BotDB

async def in_menu_back():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"sback"))
    return keyboard


async def in_menu_get_floor(floor=''):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if 'men' == floor:
        keyboard.insert(types.InlineKeyboardButton(text=f"✔️Мужчина", callback_data=f"floor mencom"))

    else:
        keyboard.insert(types.InlineKeyboardButton(text=f"Мужчина", callback_data=f"floor men"))
    if 'women' == floor:
        keyboard.insert(types.InlineKeyboardButton(text=f"✔️Женщина", callback_data=f"floor womencom"))
    else:
        keyboard.insert(types.InlineKeyboardButton(text=f"Женщина", callback_data=f"floor women"))

    if floor != '' and 'gotovo' not in floor:
        floor = f"|{floor}"
    keyboard.insert(types.InlineKeyboardButton(text=f"Готово", callback_data=f"floor gotovo" + floor))
    return keyboard

async def in_menu_set_info_users():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.insert(types.InlineKeyboardButton(text=f"Редактировать", callback_data=f"edit"))
    keyboard.insert(types.InlineKeyboardButton(text=f"Отправить", callback_data=f"nice"))
    return keyboard


async def in_menu_set_date_prognos():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.insert(types.InlineKeyboardButton(text=f"Сегодня", callback_data=f"dproc today"))
    keyboard.insert(types.InlineKeyboardButton(text=f"Завтра", callback_data=f"dproc tomorrow"))
    keyboard.insert(types.InlineKeyboardButton(text=f"На неделю", callback_data=f"dproc week"))
    keyboard.insert(types.InlineKeyboardButton(text=f"На месяц", callback_data=f"dproc month"))
    keyboard.insert(types.InlineKeyboardButton(text=f"Присылать ежедневно", callback_data=f"dproc still"))
    keyboard.insert(types.InlineKeyboardButton(text=f"Выбрать дату", callback_data=f"dproc get"))
    return keyboard
