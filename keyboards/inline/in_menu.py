import datetime

from aiogram import types

from data.config import ADMINS
from utils.db_api.db import BotDB

async def in_menu_back():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"sback"))
    return keyboard


async def in_menu_get_room():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.insert(types.InlineKeyboardButton(text=f"▫️ Малая", callback_data=f"room Малая"))
    keyboard.insert(types.InlineKeyboardButton(text=f"◽️ Модуль", callback_data=f"room Модуль"))
    keyboard.insert(types.InlineKeyboardButton(text=f"◻️ Большая", callback_data=f"room Большая"))
    return keyboard

async def get_time_in_room():
    date_h = datetime.datetime.strptime('7:30', "%H:%M")
    step = datetime.timedelta(minutes=30)
    array_date = []
    while date_h < datetime.datetime.strptime('19:30', "%H:%M"):
        date_h += step
        minute = date_h.minute
        if len(str(date_h.minute)) == 1:
            minute = '00'
        hour = f"{date_h.hour}"
        array_date.append(f"{hour}:{minute}")
    keyboard = types.InlineKeyboardMarkup(row_width=5)

    for d_i in array_date:
        keyboard.insert(types.InlineKeyboardButton(text=f"{d_i}", callback_data=f"time_h {d_i}"))
    return keyboard











async def in_menu_start(users_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text=f"🤖 Мои боты", callback_data=f"mybots {users_id}"),
                 types.InlineKeyboardButton(text=f"➕ Добавить бота", callback_data=f"addbots {users_id}"))
    if str(users_id) in ADMINS:
        keyboard.add(types.InlineKeyboardButton(text=f"📢 Оповестить админов", callback_data=f"rupor"))
    return keyboard


async def in_menu_mybots(users_id):
    get_db_telegram = BotDB()
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    array_bots_users = get_db_telegram.get_all_bots_in_user(userid=users_id)
    if array_bots_users:
        for i in array_bots_users:
            keyboard.insert(types.InlineKeyboardButton(text=f"{i['botname']}", callback_data=f"editbot {i['apitoken']}"))


    keyboard.add(types.InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"sback"))

    return keyboard



async def in_menu_back_and_send():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.insert(types.InlineKeyboardButton(text=f"Назад 🔙", callback_data=f"sback"))
    keyboard.insert(types.InlineKeyboardButton(text=f"🔜 Разослать", callback_data=f"go_send"))
    return keyboard

async def in_menu_mybots_edit(users_id, apitoken):
    get_db_telegram = BotDB()
    keyboard = types.InlineKeyboardMarkup(row_width=2)

    array_bot_user = get_db_telegram.get_bot_in_api_token(apitoken=apitoken)

    keyboard.insert(types.InlineKeyboardButton(text=f"💢 Удалить", callback_data=f"deletbot {array_bot_user['apitoken']}"))


    keyboard.insert(types.InlineKeyboardButton(text=f"🔙 Назад", callback_data=f"mybots {users_id}"))

    return keyboard