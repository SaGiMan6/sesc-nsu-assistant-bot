from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto, FSInputFile

import aiosqlite

import datetime

from menu.get_menu import get_menu, delete_menu

router = Router()


async def preparing_menu(date):
    # Узнаем у БД, есть ли на нужное число id фотографий
    db = await aiosqlite.connect("data_base/menu_data_base.db")

    await db.execute("CREATE TABLE IF NOT EXISTS Menus (date TEXT PRIMARY KEY, id TEXT)")

    cursor = await db.execute(f"SELECT date, id FROM Menus WHERE date = ?", (date,))
    result = await cursor.fetchone()

    await db.close()

    # Если в БД нашлись id, отправляем их
    # Если же в БД их нету, скачиваем фотографии
    media_group = []

    if result is None:
        menu_pages = get_menu(date)
    else:
        menu_pages = str(result[1]).split()

    if menu_pages is not None:
        for menu_page in menu_pages:
            control_page = menu_page
            if result is None:
                menu_page = FSInputFile(menu_page)

            if control_page != menu_pages[-1]:
                media_group.append(InputMediaPhoto(media=menu_page))
            else:
                media_group.append(InputMediaPhoto(media=menu_page, caption=f"Меню на {date}"))

        if result is None:
            return media_group, True, True
        else:
            return media_group, False, True
    else:
        return [], False, False


async def download_cleaning(date, result, num):
    delete_menu(date)

    sent_files = ""

    for i in range(-1, ((num + 1) * -1), -1):
        sent_files = " " + str(result[i].photo[-1].file_id) + sent_files
    id_string = sent_files.strip()

    db = await aiosqlite.connect("data_base/menu_data_base.db")

    await db.execute("INSERT INTO Menus (date, id) VALUES (?, ?)", (date, id_string))

    await db.commit()
    await db.close()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    date = str(datetime.date.today())
    result = ""

    menu_to_upload, download_used, not_empty = await preparing_menu(date)

    if not_empty:
        result = await message.answer_media_group(menu_to_upload)
    else:
        await message.answer(f"Возникла ошибка при получении меню на {date}")

    if download_used:
        await download_cleaning(date, result, len(menu_to_upload))
