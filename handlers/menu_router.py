from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import datetime

from scripts.preparing_and_cleaning_menu import preparing_menu, download_cleaning

from keyboards.keyboard_classes import MenuSimpleCallbackFactory
from keyboards.menu_keyboards import get_menu_simple_keyboard_fab

router = Router()


# async def send_menu_group(message: Message):
#     date = datetime.date.today()
#     media = True
#     result = ""
#
#     menu_to_upload, download_used, not_empty = await preparing_menu(date, media)
#     number_of_menus = len(menu_to_upload)
#
#     if not_empty:
#         result = await message.answer_media_group(menu_to_upload)
#     else:
#         await message.answer(f"Возникла ошибка при получении меню на {date.strftime(r'%d.%m.%Y')}")
#
#     if download_used:
#         await download_cleaning(result, date, number_of_menus)


async def send_menu_fab(message: Message, config, page=0, date=datetime.date.today()):
    config["date"] = date
    config["page"] = page

    result = ""

    menu_to_upload, config = await preparing_menu(config)

    print(config)
    if config["media_group"] and not config["empty"]:
        result = await message.answer_media_group(menu_to_upload)

    elif config["media_group"]:
        await message.answer(f"Возникла ошибка при получении меню на {config['date'].strftime(r'%d.%m.%Y')}")

    elif config["new_message"] and not config["empty"]:
        result = await message.answer_photo(menu_to_upload[config["page"]],

                                            caption=f"Меню на " +
                                                    f"{config['date'].strftime(r'%d.%m.%Y')} " +
                                                    f"({config['page'] + 1}/{config['number_of_pages']})",

                                            reply_markup=get_menu_simple_keyboard_fab(config["page"], config["date"],
                                                                                      config["number_of_pages"]))
    elif config["new_message"]:
        await message.answer(f"Возникла ошибка при получении меню на {config['date'].strftime(r'%d.%m.%Y')}")

    elif not config["empty"]:
        result = await message.edit_media(menu_to_upload[config["page"]],

                                          reply_markup=get_menu_simple_keyboard_fab(config["page"], config["date"],
                                                                                    config["number_of_pages"]))
        await message.edit_caption(caption=f"Меню на " +
                                           f"{config['date'].strftime(r'%d.%m.%Y')} " +
                                           f"({config['page'] + 1}/{config['number_of_pages']})",

                                   reply_markup=get_menu_simple_keyboard_fab(config["page"], config["date"],
                                                                             config["number_of_pages"]))
    else:
        await message.edit_caption(caption=f"Возникла ошибка при получении меню на " +
                                           f"{config['date'].strftime(r'%d.%m.%Y')}",

                                   reply_markup=get_menu_simple_keyboard_fab(config["page"], config["date"],
                                                                             config["number_of_pages"]))

    if config["download"] and not config["empty"]:
        await download_cleaning(result, config)


# async def edit_menu_page_fab(message: Message, config, page, date):
#     config["date"] = date
#     config["page"] = page
#
#     menu_to_upload, download_used, not_empty = await preparing_menu(date, media)
#     number_of_menus = len(menu_to_upload)
#
#     if not_empty:
#         result = await message.edit_media(menu_to_upload[page],
#                                           reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus))
#         await message.edit_caption(caption=f"Меню на {date.strftime(r'%d.%m.%Y')} ({page + 1}/{number_of_menus})",
#                                    reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus)
#     else:
#         await message.edit_caption(caption=f"Возникла ошибка при получении меню на {date.strftime(r'%d.%m.%Y')}",
#                                    reply_markup=get_menu_simple_keyboard_fab(page, date, number_of_menus)
#
#     if download_used:
#         await download_cleaning(result, date, number_of_menus)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    config = {"media_group": True,
              "new_message": True}

    await send_menu_fab(message, config)


@router.message(Command("menu_today"))
async def cmd_menu_today(message: Message):
    config = {"media_group": False,
              "new_message": True}

    await send_menu_fab(message, config)


@router.callback_query(MenuSimpleCallbackFactory.filter())
async def callbacks_menu_page_fab(callback: CallbackQuery,
                                  callback_data: MenuSimpleCallbackFactory):

    if callback_data.action == "change":
        config = {"media_group": False,
                  "new_message": False}

        await send_menu_fab(callback.message, config, callback_data.page, callback_data.date)
