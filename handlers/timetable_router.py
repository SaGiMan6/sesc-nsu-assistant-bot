from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import datetime

router = Router()


@router.message(Command("timetable"))
async def cmd_timetable(message: Message):
    print()

    # await send_timetable()