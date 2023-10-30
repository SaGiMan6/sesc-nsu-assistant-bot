from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from scripts.logging_info_out import logging_output

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    logging_output(message)

    await message.answer("""
<b>СУНЦ НГУ Помощник</b>

Этот бот создан, чтобы облегчить жизнь учащимся СУНЦ НГУ

Вы можете использовать <i>/help</i>, чтобы получить информацию о функциях бота

<u>Бот на данный момент ещё находится в разработке, функционал будет увеличиваться</u>
    """)


@router.message(Command("help"))
async def cmd_start(message: Message):
    logging_output(message)

    await message.answer("""
<b>Команды, которые на данный момент доступны:</b>

<i>/menu – Команда позволяющая узнать меню на любую дату</i>
(Нет возможности показать меню, если на эту дату оно не было опубликовано)


<b>Расширение функционала уже в разработке</b>
Планируемый функционал: 
1) Просмотр расписания
2) Рассылка с меню и расписанием
3) Оповещение о зарядке

В скором будет добавлена возможность отправлять свои вопросы, предложения и жалобы на работу бота
    """)
