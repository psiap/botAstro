import asyncio
from datetime import datetime, time

from loader import bot
from utils.db_api.db import BotDB
from utils.random_text import user_prog


async def my_function():
    get_db_telegram = BotDB()
    users = get_db_telegram.get_all_users()
    for user in users:
        if user['when_forecast'] == 'still':
            try:
                await bot.send_message(int(user['user_id']),user_prog('today', int(user['user_id'])))
            except Exception as E:
                print(E)

async def scheduler_start():
    while True:
        now = datetime.now().time()
        run_time = time(hour=8, minute=0, second=0)
        if now >= run_time:
            await my_function()
            await asyncio.sleep(86400)  # Повтор каждые 24 часа 86400
        else:
            seconds_until_run = (datetime.combine(datetime.today(), run_time) - datetime.now()).total_seconds()
            await asyncio.sleep(seconds_until_run)