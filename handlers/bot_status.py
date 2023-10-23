from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Я БЫ МОГ В ЭТО ВРЕМЯ СДЕАТЬ АНГЛИЙСКИЙ, НО ИЗ-ЗА АНТОНА МНЕ ПРИХОДИТСЯ ПРОГРАТЬ!")
