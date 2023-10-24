from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto, FSInputFile

import datetime

from scripts.interaction_with_menu_data_base import check_menu_id, add_menu_id
from scripts.get_and_delete_menu import get_menu, delete_menu

router = Router()


async def preparing_menu(date):
    result: tuple = await check_menu_id(date)

    if result is None:
        need_to_download = True
    else:
        need_to_download = False

    media_group = []

    if need_to_download:
        menu_pages = get_menu(date)
    else:
        menu_pages = str(result[1]).split()

    if menu_pages is None:
        return [], need_to_download, False
    else:
        for menu_page in menu_pages:
            control_page = menu_page
            if need_to_download:
                menu_page = FSInputFile(menu_page)

            if control_page != menu_pages[-1]:
                media_group.append(InputMediaPhoto(media=menu_page))
            else:
                media_group.append(InputMediaPhoto(media=menu_page, caption=f"Меню на {date.strftime(r'%d.%m.%Y')}"))

        return media_group, need_to_download, True


async def download_cleaning(result, date, num):
    delete_menu(date)

    sent_files = ""
    for i in range(0, num):
        sent_files = sent_files + str(result[i].photo[-1].file_id) + " "
    id_string = sent_files.strip()

    await add_menu_id(date, id_string)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    date = datetime.date.today()
    # date = datetime.date(2023, 10, 30)
    result = ""

    menu_to_upload, download_used, not_empty = await preparing_menu(date)
    number_of_menus = len(menu_to_upload)

    if not_empty:
        result = await message.answer_media_group(menu_to_upload)
    else:
        await message.answer(f"Возникла ошибка при получении меню на {date.strftime(r'%d.%m.%Y')}")

    if download_used:
        await download_cleaning(result, date, number_of_menus)
