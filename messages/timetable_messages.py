from aiogram.types import Message


class TimetableMessage:
    def __init__(self, mgs: Message):
        self.message: Message = mgs

        self.day: int = 0
        self.need_all_week: bool = False
        self.

    def get_processed_timetable(self):
