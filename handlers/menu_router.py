from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import datetime

from scripts.preparing_and_cleaning_menu import preparing_menu, download_cleaning

from keyboards.keyboard_classes import MenuSimpleCallbackFactory
from keyboards.menu_keyboards import get_menu_simple_keyboard_fab

router = Router()


async def send_menu_group(message: Message):
    date = datetime.date.today()
    media = True
    result = ""

    menu_to_upload, download_used, not_empty = await preparing_menu(date, media)
    number_of_menus = len(menu_to_upload)

    if not_empty:
        result = await message.answer_media_group(menu_to_upload)
    else:
        await message.answer(f"Возникла ошибка при получении меню на {date.strftime(r'%d.%m.%Y')}")

    if download_used:
        await download_cleaning(result, date, number_of_menus)


async def send_menu_page_fab(message: Message):
    date = datetime.date.today()
    media = False
    result = ""
    page = 0

    menu_to_upload, download_used, not_empty = await preparing_menu(date, media)
    number_of_menus = len(menu_to_upload)

    if not_empty:
        result = await message.answer_photo(menu_to_upload[page],
                                            caption=f"Меню на " +
                                                    f"{date.strftime(r'%d.%m.%Y')} " +
                                                    f"({page + 1}/{number_of_menus})",
                                            reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus))
    else:
        await message.answer(f"Возникла ошибка при получении меню на {date.strftime(r'%d.%m.%Y')}")

    if download_used:
        await download_cleaning(result, date, number_of_menus)


async def edit_menu_page_fab(message: Message, page, date):
    media = True
    result = ""

    menu_to_upload, download_used, not_empty = await preparing_menu(date, media)
    number_of_menus = len(menu_to_upload)

    if not_empty:
        result = await message.edit_media(menu_to_upload[page],
                                          reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus))
        await message.edit_caption(caption=f"Меню на {date.strftime(r'%d.%m.%Y')} ({page + 1}/{number_of_menus})",
                                   reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus))
    else:
        await message.edit_caption(caption=f"Возникла ошибка при получении меню на {date.strftime(r'%d.%m.%Y')}",
                                   reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus))

    if download_used:
        await download_cleaning(result, date, number_of_menus)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    await send_menu_group(message)


@router.message(Command("menu_today"))
async def cmd_menu_today(message: Message):
    await send_menu_page_fab(message)


@router.callback_query(MenuSimpleCallbackFactory.filter())
async def callbacks_menu_page_fab(callback: CallbackQuery,
                                  callback_data: MenuSimpleCallbackFactory):

    if callback_data.action == "change":
        await edit_menu_page_fab(callback.message, callback_data.page, callback_data.date)
