from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery


from messages.menu_messages import SingleMenuMessage, GroupMenuMessage, CalendarMenuMessage

from keyboards.menu_keyboard_classes import MenuSimpleCallbackFactory, MenuCalendarCallbackFactory

from scripts.logging_info_out import logging_output

router = Router()


@router.message(Command("menu_group"))
async def cmd_menu_group(message: Message):
    logging_output(message)

    menu_message = GroupMenuMessage(message)

    await menu_message.get_processed_menu()
    await menu_message.send_message()


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    logging_output(message)

    menu_message = SingleMenuMessage(message)

    await menu_message.get_processed_menu()
    await menu_message.send_message()


@router.callback_query(MenuSimpleCallbackFactory.filter())
async def callbacks_menu_page_fab(callback: CallbackQuery,
                                  callback_data: MenuSimpleCallbackFactory):
    logging_output(callback.message)

    if callback_data.action == "change":
        menu_message = SingleMenuMessage(callback.message)

        menu_message.date = callback_data.date
        menu_message.page = callback_data.page
        menu_message.new_message = False

        await menu_message.get_processed_menu()
        await menu_message.send_message()

        await callback.answer()

    if callback_data.action == "calendar":
        calendar_message = CalendarMenuMessage(callback.message, callback_data.date)

        await callback.message.delete()

        await calendar_message.send_message()
        await callback.answer()


@router.callback_query(MenuCalendarCallbackFactory.filter())
async def callbacks_menu_calendar_fab(callback: CallbackQuery,
                                      callback_data: MenuCalendarCallbackFactory):
    logging_output(callback.message)

    if callback_data.action == "date":
        menu_message = SingleMenuMessage(callback.message)

        menu_message.date = callback_data.date

        await menu_message.get_processed_menu()
        await callback.message.delete()
        await menu_message.send_message()

        await callback.answer()

    if callback_data.action == "change":
        calendar_message = CalendarMenuMessage(callback.message, callback_data.date)

        calendar_message.new_message = False

        await calendar_message.send_message()
        await callback.answer()

    if callback_data.action == "nothing":
        await callback.answer()
