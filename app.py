import asyncio

from aiogram import executor

from loader import dp
import middlewares, filters, handlers

from utils.notify_admins import on_startup_notify
from utils.scheduler import scheduler_start
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)

    await on_startup_notify(dispatcher)
    asyncio.create_task(scheduler_start())

#test1

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup,skip_updates=True)
