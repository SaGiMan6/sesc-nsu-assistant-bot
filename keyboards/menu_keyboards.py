import datetime

from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.menu_keyboard_classes import MenuSimpleCallbackFactory, MenuCalendarCallbackFactory


def create_date_config(date: datetime.date):
    new_config = dict()

    new_config["year"] = int(date.strftime(r"%Y"))
    new_config["month"] = int(date.strftime(r"%m"))
    new_config["day"] = int(date.strftime(r"%d"))

    new_config["months"] = ["☃️ Январь", "❄️ Февраль", "🌷 Март", "💮 Апрель", "🌸 Май", "🍧 Июнь",
                            "🏖️ Июль", "🌻 Август", "🍁 Сентябрь", "🕸️ Октябрь", "🌧️ Ноябрь", "⛄ Декабрь"]

    if new_config["month"] != 12:
        new_config["days_in_month"] = (datetime.date(new_config["year"], new_config["month"] + 1, 1) -
                                       datetime.date(new_config["year"], new_config["month"], 1)).days
    else:
        new_config["days_in_month"] = (datetime.date(new_config["year"] + 1, 1, 1) -
                                       datetime.date(new_config["year"], new_config["month"], 1)).days

    new_config["first_week_day_in_month"] = (int(datetime.date(new_config["year"], new_config["month"], 1).strftime(
        r"%w")) - 1) % 7

    new_config["strings_in_calendar"] = (new_config["first_week_day_in_month"] + new_config["days_in_month"] + 6) // 7

    new_config["last_days"] = ((new_config["strings_in_calendar"] * 7) -
                               (new_config["first_week_day_in_month"] + new_config["days_in_month"]))

    new_config["days_in_week"] = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

    new_config["delta_plus"] = datetime.timedelta(days=(45 - new_config["day"]))
    new_config["delta_minus"] = datetime.timedelta(days=(new_config["day"] + 15))

    return new_config


def get_menu_simple_keyboard_fab(page, date, number_of_pages):
    builder = InlineKeyboardBuilder()

    if number_of_pages > 0:
        builder.button(
            text="⏪ Страница", callback_data=MenuSimpleCallbackFactory(action="change",
                                                                       page=((page - 1) % number_of_pages),
                                                                       date=date)
        )
        builder.button(
            text="Страница ⏩", callback_data=MenuSimpleCallbackFactory(action="change",
                                                                       page=((page + 1) % number_of_pages),
                                                                       date=date)
        )
    builder.button(
        text="🗓️ Календарь", callback_data=MenuSimpleCallbackFactory(action="calendar",
                                                                     date=date)
    )

    builder.adjust(2)
    return builder.as_markup()


def get_menu_calendar_keyboard_fab(date: datetime.date):
    config: dict = create_date_config(date)

    builder_1 = InlineKeyboardBuilder()
    builder_1.button(
        text=f"{config['months'][config['month'] - 1]} {config['year']}",
        callback_data=MenuCalendarCallbackFactory(action="nothing")
    )
    builder_1.adjust(1)

    builder_2 = InlineKeyboardBuilder()
    for i in range(7):
        builder_2.button(
            text=config["days_in_week"][i],
            callback_data=MenuCalendarCallbackFactory(action="nothing")
        )

    for i in range(config["first_week_day_in_month"]):
        builder_2.button(
            text=" ",
            callback_data=MenuCalendarCallbackFactory(action="nothing")
        )

    for i in range(config["days_in_month"]):

        key_day = f"{i + 1}"

        builder_2.button(
            text=key_day,
            callback_data=MenuCalendarCallbackFactory(action="date", date=datetime.date(config["year"],
                                                                                        config["month"],
                                                                                        i + 1))
        )

    for i in range(config["last_days"]):
        builder_2.button(
            text=" ",
            callback_data=MenuCalendarCallbackFactory(action="nothing")
        )
    builder_2.adjust(7)

    builder_3 = InlineKeyboardBuilder()
    builder_3.button(
        text="⏪ Месяц",
        callback_data=MenuCalendarCallbackFactory(action="change", date=(date - config["delta_minus"]))
    )
    builder_3.button(
        text="⏩ Месяц",
        callback_data=MenuCalendarCallbackFactory(action="change", date=(date + config["delta_plus"]))
    )
    builder_3.adjust(2)

    builder_all = InlineKeyboardBuilder()
    builder_all.attach(builder_1)
    builder_all.attach(builder_2)
    builder_all.attach(builder_3)

    return builder_all.as_markup()
