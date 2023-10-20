from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto, FSInputFile

import datetime

from menu.get_menu import get_menu


router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    menu_lists = get_menu()
    menu_to_upload = []

    for menu_list in menu_lists:
        file = FSInputFile(menu_list)
        if menu_list != menu_lists[-1]:
            menu_to_upload.append(InputMediaPhoto(media=file))
        else:
            menu_to_upload.append(InputMediaPhoto(media=file, caption=f"Меню на {str(datetime.date.today())}"))

    await message.answer_media_group(menu_to_upload)
