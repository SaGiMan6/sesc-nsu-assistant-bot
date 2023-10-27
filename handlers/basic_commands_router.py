from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("""
<b>СУНЦ НГУ Помощник</b>

Этот бот создан, чтобы облегчить жизнь учащимся СУНЦ НГУ

Вы можете использовать <i>/help</i>, чтобы получить информацию о функциях бота

Наш бот для обратной связи – <i>@sesc_nsu_support_bot</i>
Напишите ему пожалуйста, если столкнулись с проблемами в работе бота
Также вы можете написать ему свои вопросы, предложения
    """)


@router.message(Command("help"))
async def cmd_start(message: Message):
    await message.answer("""
<b>Команды, которые на данный момент доступны:</b>

<i>/menu – Команда позволяющая узнать меню на любую дату</i>
(Нет возможности показать меню, если на эту дату оно не было опубликовано)
    """)
