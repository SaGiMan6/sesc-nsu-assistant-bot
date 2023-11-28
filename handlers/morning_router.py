from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from scripts.morning_exercise_operations import set_morning_trigger


router = Router()


@router.message(Command("morning"))
async def cmd_morning(message: Message):
    async def function(string):
        await message.answer(string)
    await set_morning_trigger(function)


