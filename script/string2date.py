from datetime import datetime

from re import match, sub


def string2date(string: str):
    date = datetime.now().strftime(r"%d %m %y").split()
    string = string.lower()
    monthes = ["янв", "фев", "мар", "апр", "май", "июн", "июл", "авг", "сен", "окт", "ноя", "дек"]
    for i in range(len(monthes)):
        if string.find(monthes[i]) != -1:
            date[1] = str(i)
    string = sub(r"[^\d]", r" ", string).strip().split()
    for i in range(len(string)):
        date[i] = string[i]
    if match(r"\d\d\d\d", date[2]):
        string[2] = date[2][-2:]
    return datetime(int(date[2]), int(date[1]), int(date[0]))
