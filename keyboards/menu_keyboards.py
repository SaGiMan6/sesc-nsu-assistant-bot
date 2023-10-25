import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.keyboard_classes import MenuSimpleCallbackFactory


def get_menu_simple_keyboard_fab(page, date, number):
    if number == 0:
        number += 1

    builder = InlineKeyboardBuilder()
    delta = datetime.timedelta(days=1)

    builder.button(
        text="Пред. стр.", callback_data=MenuSimpleCallbackFactory(action="change",
                                                                   page=((page - 1) % number),
                                                                   date=date)
    )
    builder.button(
        text="След. стр.", callback_data=MenuSimpleCallbackFactory(action="change",
                                                                   page=((page + 1) % number),
                                                                   date=date)
    )
    builder.button(
        text="Пред. день", callback_data=MenuSimpleCallbackFactory(action="change",
                                                                   page=0,
                                                                   date=date - delta)
    )
    builder.button(
        text="След. день", callback_data=MenuSimpleCallbackFactory(action="change",
                                                                   page=0,
                                                                   date=date + delta)
    )
    builder.button(
        text="Открыть календарь", callback_data=MenuSimpleCallbackFactory(action="calendar")
    )

    builder.adjust(2)
    return builder.as_markup()
