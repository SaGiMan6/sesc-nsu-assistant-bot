from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import aiofiles

import datetime

import json

from scripts.preparing_and_cleaning_menu import preparing_menu, download_cleaning

from keyboards.keyboard_classes import MenuSimpleCallbackFactory, MenuCalendarCallbackFactory
from keyboards.menu_keyboards import get_menu_simple_keyboard_fab, get_menu_calendar_keyboard_fab

router = Router()


async def send_menu_fab(message: Message, config, date=datetime.date.today(), page=0):
    config["date"] = date
    config["page"] = page

    result = ""

    menu_to_upload, config = await preparing_menu(config)

    if config["media_group"] and not config["empty"]:
        result = await message.answer_media_group(menu_to_upload)

    elif config["media_group"]:
        await message.answer(f"Возникла ошибка при получении меню на " +
                             f"{config['date'].strftime(r'%d.%m.%Y')}")

    elif config["new_message"] and not config["empty"]:
        result = await message.answer_photo(menu_to_upload[config["page"]],
                                            caption=f"Меню на " +
                                                    f"{config['date'].strftime(r'%d.%m.%Y')} " +
                                                    f"({config['page'] + 1}/" +
                                                    f"{config['number_of_pages']})",
                                            reply_markup=get_menu_simple_keyboard_fab(config["page"],
                                                                                      config["date"],
                                                                                      config["number_of_pages"]))
    elif config["new_message"]:
        async with aiofiles.open('private_config.json', 'r') as file:
            read_file = await file.read()
            photo_id: str = json.loads(read_file)["ERROR_PHOTO_ID"]

        result = await message.answer_photo(photo_id,
                                            caption=f"Возникла ошибка при получении меню на " +
                                                    f"{config['date'].strftime(r'%d.%m.%Y')}",
                                            reply_markup=get_menu_simple_keyboard_fab(config["page"],
                                                                                      config["date"],
                                                                                      config["number_of_pages"],
                                                                                      False))
    elif not config["empty"]:
        result = await message.edit_media(menu_to_upload[config["page"]],
                                          reply_markup=get_menu_simple_keyboard_fab(config["page"],
                                                                                    config["date"],
                                                                                    config["number_of_pages"]))
        await message.edit_caption(caption=f"Меню на " +
                                           f"{config['date'].strftime(r'%d.%m.%Y')} " +
                                           f"({config['page'] + 1}/" +
                                           f"{config['number_of_pages']})",
                                   reply_markup=get_menu_simple_keyboard_fab(config["page"],
                                                                             config["date"],
                                                                             config["number_of_pages"]))
    else:
        await message.edit_caption(caption=f"Возникла ошибка при получении меню на " +
                                           f"{config['date'].strftime(r'%d.%m.%Y')}",
                                   reply_markup=get_menu_simple_keyboard_fab(config["page"], config["date"],
                                                                             config["number_of_pages"]))

    if config["download"] and not config["empty"]:
        await download_cleaning(message, result, config)


async def send_calendar_fab(message: Message, date: datetime.date, edit: bool):
    if edit:
        await message.edit_reply_markup(reply_markup=get_menu_calendar_keyboard_fab(date))
    else:
        await message.delete()
        await message.answer("Выберите нужную вам дату",
                             reply_markup=get_menu_calendar_keyboard_fab(date))


@router.message(Command("menu_group"))
async def cmd_menu_group(message: Message):
    print(f"User id: {message.from_user.id}, Username: {message.from_user.username}")
    print(f"First name: {message.from_user.first_name}, Last name: {message.from_user.last_name}")
    print("/menu_group")

    config = {"media_group": True,
              "new_message": True}

    await send_menu_fab(message, config)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    print(f"User id: {message.from_user.id}, Username: {message.from_user.username}")
    print(f"First name: {message.from_user.first_name}, Last name: {message.from_user.last_name}")
    print("/menu")

    config = {"media_group": False,
              "new_message": True}

    await send_menu_fab(message, config)


@router.callback_query(MenuSimpleCallbackFactory.filter())
async def callbacks_menu_page_fab(callback: CallbackQuery,
                                  callback_data: MenuSimpleCallbackFactory):
    print(f"User id: {callback.from_user.id}, Username: {callback.from_user.username}")
    print(f"First name: {callback.from_user.first_name}, Last name: {callback.from_user.last_name}")
    print("Menu_callback")

    if callback_data.action == "change":
        config = {"media_group": False,
                  "new_message": False}

        await send_menu_fab(callback.message, config, callback_data.date, callback_data.page)
        await callback.answer()

    if callback_data.action == "calendar":
        await send_calendar_fab(callback.message, callback_data.date, False)
        await callback.answer()


@router.callback_query(MenuCalendarCallbackFactory.filter())
async def callbacks_menu_calendar_fab(callback: CallbackQuery,
                                      callback_data: MenuCalendarCallbackFactory):
    print(f"User id: {callback.from_user.id}, Username: {callback.from_user.username}")
    print(f"First name: {callback.from_user.first_name}, Last name: {callback.from_user.last_name}")
    print("Calendar_callback")

    if callback_data.action == "date":
        config = {"media_group": False,
                  "new_message": True}

        await callback.message.delete()
        await send_menu_fab(callback.message, config, callback_data.date)
        await callback.answer()

    if callback_data.action == "change":
        await send_calendar_fab(callback.message, callback_data.date, True)
        await callback.answer()

    if callback_data.action == "nothing":
        await callback.answer()
