import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

import configparser

private_config = configparser.ConfigParser()
private_config.read("private_Config.ini")


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=private_config["token"]["BOT_TOKEN"])
    dp = Dispatcher()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
