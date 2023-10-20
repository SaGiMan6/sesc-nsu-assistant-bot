from aiogram import Router, F
from aiogram.enums import InputMediaType
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, InputFile, InputMediaPhoto

from menu.get_menu import get_menu


router = Router()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    menu_data = get_menu()
    data_to_upload = []

    for i in range(len(menu_data)):
        data_to_upload.append(InputMediaPhoto(media="E:\Programming\sesc-nsu-assistant-bot\menu\menu_20.10.23_page_0.jpg"))

    await message.answer_media_group(data_to_upload)
