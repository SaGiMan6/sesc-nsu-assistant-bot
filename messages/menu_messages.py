from aiogram.types import Message, FSInputFile, InputMediaPhoto

import aiofiles

import json

import datetime

from scripts.menu_data_base_interaction import check_menu_id, add_menu_id
from scripts.menu_operations import get_menu, delete_menu

from keyboards.menu_keyboards import get_menu_simple_keyboard_fab, get_menu_calendar_keyboard_fab


class MenuMessage:
    def __init__(self, msg: Message):
        self.message: Message = msg

        self.date: datetime.date = datetime.date.today()
        self.page: int = 0

        self.db_result = None
        self.need_downloading = False
        self.menu_pages = []
        self.number_of_pages = 0
        self.sending_result = None

    async def get_processed_menu(self):
        self.db_result: tuple = await check_menu_id(self.date)

        if self.db_result is None:
            self.need_downloading = True
            pages = get_menu(self.date)
            if pages is not None:
                self.menu_pages = [(lambda page: FSInputFile(page))(page) for page in pages]
        else:
            self.menu_pages = str(self.db_result[1]).split()


class SingleMenuMessage(MenuMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)

        self.new_message = True

    async def send_message(self):
        self.number_of_pages = len(self.menu_pages)

        if not self.menu_pages:
            async with aiofiles.open("private_config.json", "r") as file:
                read_file = await file.read()
                error_photo_id: str = json.loads(read_file)["ERROR_PHOTO_ID"]

            if self.new_message:
                await self.message.answer_photo(error_photo_id,
                                                caption=f"Возникла ошибка при получении меню на " +
                                                        f"{self.date.strftime(r'%d.%m.%Y')}",
                                                reply_markup=get_menu_simple_keyboard_fab(self.page,
                                                                                          self.date,
                                                                                          self.number_of_pages))
            else:
                await self.message.edit_media(InputMediaPhoto(media=error_photo_id,
                                                              caption=f"Возникла ошибка при получении меню на " +
                                                                      f"{self.date.strftime(r'%d.%m.%Y')}"),
                                              reply_markup=get_menu_simple_keyboard_fab(self.page,
                                                                                        self.date,
                                                                                        self.number_of_pages))
        else:
            if self.new_message:
                await self.message.answer_photo(self.menu_pages[self.page],
                                                caption=f"Меню на " +
                                                        f"{self.date.strftime(r'%d.%m.%Y')} " +
                                                        f"({self.page + 1}/" +
                                                        f"{self.number_of_pages})",
                                                reply_markup=get_menu_simple_keyboard_fab(self.page,
                                                                                          self.date,
                                                                                          self.number_of_pages))
            else:
                await self.message.edit_media(InputMediaPhoto(media=self.menu_pages[self.page],
                                                              caption=f"Меню на " +
                                                                      f"{self.date.strftime(r'%d.%m.%Y')} " +
                                                                      f"({self.page + 1}/" +
                                                                      f"{self.number_of_pages})"),
                                              reply_markup=get_menu_simple_keyboard_fab(self.page,
                                                                                        self.date,
                                                                                        self.number_of_pages))

            if self.need_downloading:
                delete_menu(self.date)

                menu_message = GroupMenuMessage(self.message)

                async with aiofiles.open('private_config.json', 'r') as file:
                    read_file = await file.read()
                    spam_chat_id: int = json.loads(read_file)["SPAM_USER_ID"]

                menu_message.date = self.date
                menu_message.chat_id = spam_chat_id

                await menu_message.get_processed_menu()
                await menu_message.send_message()


class GroupMenuMessage(MenuMessage):
    def __init__(self, msg: Message):
        super().__init__(msg)

        self.chat_id = None

    async def send_message(self):
        if not self.menu_pages:
            async with aiofiles.open("private_config.json", "r") as file:
                read_file = await file.read()
                error_photo_id: str = json.loads(read_file)["ERROR_PHOTO_ID"]

            await self.message.answer_photo(error_photo_id,
                                            caption=f"Возникла ошибка при получении меню на " +
                                                    f"{self.date.strftime(r'%d.%m.%Y')}",
                                            reply_markup=get_menu_simple_keyboard_fab(self.page,
                                                                                      self.date,
                                                                                      self.number_of_pages))
        else:
            for number, page in enumerate(self.menu_pages):
                if number < (len(self.menu_pages) - 1):
                    self.menu_pages[number] = InputMediaPhoto(media=page)
                else:
                    self.menu_pages[number] = InputMediaPhoto(media=page,
                                                              caption=f"Меню на {self.date.strftime(r'%d.%m.%Y')}")

            if self.chat_id is None:
                self.sending_result = await self.message.answer_media_group(self.menu_pages)
            else:
                self.sending_result = await self.message.bot.send_media_group(self.chat_id, self.menu_pages)

            if self.need_downloading:
                delete_menu(self.date)

                sent_files = ""
                for i in range(len(self.menu_pages)):
                    sent_files = sent_files + str(self.sending_result[i].photo[-1].file_id) + " "
                id_string = sent_files.strip()

                await add_menu_id(self.date, id_string)


class CalendarMenuMessage:
    def __init__(self, msg: Message, dt: datetime.date):
        self.calendar_message = msg
        self.date = dt

        self.new_message = True

    async def send_message(self):
        if self.new_message:
            await self.calendar_message.answer("Выберите нужную вам дату",
                                               reply_markup=get_menu_calendar_keyboard_fab(self.date))
        else:
            await self.calendar_message.edit_reply_markup(reply_markup=get_menu_calendar_keyboard_fab(self.date))
