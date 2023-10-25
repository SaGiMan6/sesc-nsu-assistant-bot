from aiogram.filters.callback_data import CallbackData

from typing import Optional

import datetime


class MenuSimpleCallbackFactory(CallbackData, prefix="menu_simple"):
    action: str
    page: Optional[int] = None
    date: Optional[datetime.date] = None
