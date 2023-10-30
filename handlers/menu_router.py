from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import datetime

from messages.menu_messages import SingleMenuMessage, GroupMenuMessage

from keyboards.menu_keyboard_classes import MenuSimpleCallbackFactory, MenuCalendarCallbackFactory
from keyboards.menu_keyboards import get_menu_calendar_keyboard_fab

router = Router()


async def send_calendar_fab(message: Message, date: datetime.date, edit: bool):
    if edit:
        await message.edit_reply_markup(reply_markup=get_menu_calendar_keyboard_fab(date))
    else:
        await message.delete()
        await message.answer("Выберите нужную вам дату",
                             reply_markup=get_menu_calendar_keyboard_fab(date))


@router.message(Command("menu_group"))
async def cmd_menu_group(message: Message):
    menu_message = GroupMenuMessage(message)

    await menu_message.get_processed_menu()
    await menu_message.send_message()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    menu_message = SingleMenuMessage(message)

    await menu_message.get_processed_menu()
    await menu_message.send_message()


@router.callback_query(MenuSimpleCallbackFactory.filter())
async def callbacks_menu_page_fab(callback: CallbackQuery,
                                  callback_data: MenuSimpleCallbackFactory):
    if callback_data.action == "change":
        menu_message = SingleMenuMessage(callback.message)

        menu_message.date = callback_data.date
        menu_message.page = callback_data.page
        menu_message.new_message = False

        await menu_message.get_processed_menu()
        await menu_message.send_message()

        await callback.answer()

    if callback_data.action == "calendar":
        await send_calendar_fab(callback.message, callback_data.date, False)
        await callback.answer()


@router.callback_query(MenuCalendarCallbackFactory.filter())
async def callbacks_menu_calendar_fab(callback: CallbackQuery,
                                      callback_data: MenuCalendarCallbackFactory):
    if callback_data.action == "date":
        menu_message = SingleMenuMessage(callback.message)

        menu_message.date = callback_data.date

        await menu_message.get_processed_menu()
        await callback.message.delete()
        await menu_message.send_message()

        await callback.answer()

    if callback_data.action == "change":
        await send_calendar_fab(callback.message, callback_data.date, True)
        await callback.answer()

    if callback_data.action == "nothing":
        await callback.answer()
