import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import bot_status, bot_menu

import json

with open('private_config.json', 'r') as file:
    token = json.load(file)["BOT_TOKEN"]


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(bot_status.router, bot_menu.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
