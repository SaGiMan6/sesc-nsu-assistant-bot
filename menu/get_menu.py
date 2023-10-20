from os import remove
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
        names[i] = 'menu/' + 'menu_' + date + '_page_' + str(i) + '.jpg'
        menu_files[i].save(names[i], 'JPEG')

    return names


def get_data():
    if not isfile('menu/data.json'):
        with open('menu/data.json', 'w') as file:
            data = {'date': '', 'names': []}
            dump(data, file)
    with open('menu/data.json', 'r') as file:
        return load(file)

def remove_trash(names):
    for i in names:
        remove(i)

def write_data(data={'date': '', 'names': []}):
    with open('menu/data.json', 'w') as file:
        dump(data, file)

def get_menu(date=dateNow()):
    data = get_data()
    if date != data['date']:
        names = download_menu(date)
        if names == None:
            return []
        else:
            write_data({'date': date, 'names': names})
            remove_trash(data['names'])
            return names
    else:
        return data['names']


if __name__ == "__main__":
    get_menu()
