from aiogram.filters.callback_data import CallbackData

from typing import Optional

import datetime


class MenuSimpleCallbackFactory(CallbackData, prefix="menu_simple"):
    action: str
    page: Optional[int] = None
    date: datetime.date


class MenuCalendarCallbackFactory(CallbackData, prefix="menu_calendar"):
    action: str
    date: Optional[datetime.date] = None
