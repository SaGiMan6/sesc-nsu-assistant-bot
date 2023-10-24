import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import basic_commands_router, menu_router

import json

with open('private_config.json', 'r') as file:
    token: str = json.load(file)["BOT_TOKEN"]


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_routers(basic_commands_router.router, menu_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
