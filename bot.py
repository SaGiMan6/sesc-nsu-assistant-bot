import asyncio
import logging

from aiogram import Bot, Dispatcher

from handlers import basic_router, timetable_router, menu_router

import json

with open('private_config.json', 'r') as file:
    token: str = json.load(file)["BOT_TOKEN"]


logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher()

    dp.include_routers(basic_router.router,
                       timetable_router.router,
                       menu_router.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
