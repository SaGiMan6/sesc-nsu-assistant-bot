from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto, FSInputFile

from menu.get_menu import get_menu


router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    menu_data = get_menu()
    data_to_upload = []

    for i in range(len(menu_data)):
        file = FSInputFile(menu_data[i])
        data_to_upload.append(InputMediaPhoto(media=file))

    await message.answer_media_group(data_to_upload)
