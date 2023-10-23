from shutil import rmtree

from os import mkdir

from requests import get

from re import search, escape, match

from pdf2image import convert_from_bytes

from datetime import datetime

path = 'menu/'


def date_now():
    return str(datetime.now().date())


def norm_date(date):
    if match(r"\d\d\d\d-\d\d-\d\d", date):
        date = date[-2:] + "." + date[-5:-3] + "." + date[-8:-6]
        return date
    elif match(r"\d\d\.\d\d\.\d\d", date):
        return date
    else:
        raise ValueError("Date format is wrong.")


def delete_menu(date=date_now()):
    date = norm_date(date)
    rmtree(path + "menu_" + date)


def get_menu(date=date_now()):
    date = norm_date(date)
    link = "https://sesc.nsu.ru/sveden/food/"
    try:
        response = get(link)
    except:
        return None
    html = str(response.text)
    start = escape("upload/iblock/")
    end = escape("menu_" + date + ".pdf")
    link = search(fr"{start}\S+{end}", html)
    if link is None:
        return None
    link = "https://sesc.nsu.ru/" + link.group(0)
    try:
        response = get(link)
    except:
        return None
    menu_files = convert_from_bytes(response.content)
    mkdir(path + "menu_" + date)
    names = ['' for _ in range(len(menu_files))]
    for i in range(len(menu_files)):
        names[i] = path + "menu_" + date + "/" + str(i) + ".jpg"
        menu_files[i].save(names[i], "JPEG")

    return names


if __name__ == "__main__":
    path = ""
    get_menu()
    # delete_menu()
