from requests import get
from json import dump, load
from datetime import datetime
from re import search, escape
from pdf2image import convert_from_bytes

date = str(datetime.now().date())
date = date[-2:] + '.' + date[-5:-3] + '.' + date[-8:-6]

def downloadMenu():
    html = str(get('https://sesc.nsu.ru/sveden/food/').text)
    start = escape('upload/iblock/')
    end = escape('menu_' + date + '.pdf')
    link = 'https://sesc.nsu.ru/' + search(fr'{start}\S+{end}', html).group(0)
    menu_files = convert_from_bytes(get(link).content)

    names = ['' for i in range(len(menu_files))]
    for i in range(len(menu_files)):
        names[i] = 'menu_' + date + '_page_' + str(i) + '.jpg'
        menu_files[i].save(names[i], 'JPEG')

    return names

def lastDownloadDate():
    with open('data.json', 'r') as file:
        if file.read():
            return load(file)['date']
    return None

def getMenu():
    with open('data.json', 'w') as file:
        pass
    if lastDownloadDate() != date:
        with open('data.json', 'w') as file:
            names = downloadMenu()
            data = {'date': date, 'names': names}
            dump(data, file)
