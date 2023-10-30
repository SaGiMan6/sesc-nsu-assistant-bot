from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    print(f"User id: {message.from_user.id}, Username: {message.from_user.username}")
    print(f"First name: {message.from_user.first_name}, Last name: {message.from_user.last_name}")
    print("/start")

    await message.answer("""
<b>СУНЦ НГУ Помощник</b>

Этот бот создан, чтобы облегчить жизнь учащимся СУНЦ НГУ

Вы можете использовать <i>/help</i>, чтобы получить информацию о функциях бота

<b>(Бот на данный момент находится в разработке, функционал будет увеличиваться):</b>
    """)


@router.message(Command("help"))
async def cmd_start(message: Message):
    print(f"User id: {message.from_user.id}, Username: {message.from_user.username}")
    print(f"First name: {message.from_user.first_name}, Last name: {message.from_user.last_name}")
    print("/help")
    
    await message.answer("""
<b>Команды, которые на данный момент доступны:</b>

<i>/menu – Команда позволяющая узнать меню на любую дату</i>
(Нет возможности показать меню, если на эту дату оно не было опубликовано)

<b>Расширение функционала уже в разработке</b>
Планируемый дополнительный функционал: 
1) Просмотр расписания
2) Рассылка с меню и расписанием
3) Оповещение о зарядке

В скором будет добавлена возможность отправлять свои вопросы, предложения и жалобы на работу бота
    """)
