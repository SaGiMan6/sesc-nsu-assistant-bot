from os import remove, stat
from os.path import isfile

from requests import get

from re import search, escape

from pdf2image import convert_from_bytes

from json import dump, load

from datetime import datetime

def dateNow():
    date = str(datetime.now().date())
    date = date[-2:] + '.' + date[-5:-3] + '.' + date[-8:-6]
    return date

def download_menu(date=dateNow()):
    link = 'https://sesc.nsu.ru/sveden/food/'
    try:
        response = get(link)
    except:
        return None
    html = str(response.text)
    start = escape('upload/iblock/')
    end = escape('menu_' + date + '.pdf')
    link = search(fr'{start}\S+{end}', html)
    if link == None:
        return None
    link = 'https://sesc.nsu.ru/' + link.group(0)
    try:
        response = get(link)
    except:
        return None
    menu_files = convert_from_bytes(response.content)
    names = ['' for i in range(len(menu_files))]
    for i in range(len(menu_files)):
        names[i] = 'menu_' + date + '_page_' + str(i) + '.jpg'
        menu_files[i].save(names[i], 'JPEG')

    return names


def last_download_date():
    if stat('data.json').st_size != 0:
        with open('data.json', 'r') as file:
            return load(file)['date']

    return None


def last_names():
    if stat('data.json').st_size != 0:
        with open('data.json', 'r') as file:
            return load(file)['names']

    return []


def get_menu(date=dateNow()):
    if not isfile('data.json'):
        with open('data.json', 'w') as file:
            pass

    if last_download_date() != date:
        names = download_menu(date)
        if names != None:
            for i in last_names():
                remove(i)

            with open('data.json', 'w') as file:
                data = {'date': date, 'names': names}
                dump(data, file)
        else:
            return []

    return last_names()


if __name__ == "__main__":
    print(get_menu())
