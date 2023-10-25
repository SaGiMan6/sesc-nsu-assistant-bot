from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Этот бот создан для помощи учащимся СУНЦ НГУ \n\n" +
                         "На данный момент работают команды:\n" +
                         "/menu – Команда, чтобы узнать меню столовой")
