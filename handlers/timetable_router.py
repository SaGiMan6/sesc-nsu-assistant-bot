from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

import datetime

router = Router()


@router.message(Command("timetable"))
async def cmd_timetable(message: Message):
    await message.answer("""<code>+-------------+
|    11-10    |
+-------------+
|     321     |
+-------------+
| ФИЗ   – 251 |
| МАТ   – 160 |
| МАТ Л – 251 |
+-------------+
</code>""")
