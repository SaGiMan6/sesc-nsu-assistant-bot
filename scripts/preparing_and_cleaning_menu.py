from aiogram.types import InputMediaPhoto, FSInputFile

from scripts.interaction_with_menu_data_base import check_menu_id, add_menu_id
from scripts.get_and_delete_menu import get_menu, delete_menu


async def preparing_menu(config: dict):
    # Запрос к БД на наличие id фотографий меню на требуемую дату
    db_result: tuple = await check_menu_id(config["date"])

    # Если запрос вернул None, записываем в конфиг, что потребуется загрузка из источника
    if db_result is None:
        config["download"] = True
    # Иначе указываем, что загрузка не потребуется
    else:
        config["download"] = False

    # Если требуется загрузка, скачиваем с помощью get_menu, и записываем пути к файлам
    if config["download"]:
        menu_pages = get_menu(config["date"])
    # Иначе записываем id файлов, полученные из БД
    else:
        menu_pages = str(db_result[1]).split()

    # Если menu_pages является None, значит не удалось скачать из источника,
    # Тогда добавляем в конфиг информацию о том, что получить меню не удалось,
    # И возвращаем его вместе с пусто строкой
    if menu_pages is None:
        config["empty"] = True
        config["number_of_pages"] = 0

        return [], config
    # Иначе преобразуем пути к файлам/id файлов в типы данных, требуемые для отправки
    else:
        config["empty"] = False
        list_of_files = []
        # Если было произведено скачивание, импортируем файлы с помощью FSInputFile()
        if config["download"]:
            for number, menu_page in enumerate(menu_pages):
                menu_pages[number] = FSInputFile(menu_page)

        # Если нужно отправить сообщение с группой файлов, составляем список из файлов,
        # Обработанных с помощью InputMediaPhoto, ставим подпись к последнему
        if config["media_group"]:
            for menu_page in menu_pages:
                if menu_page != menu_pages[-1]:
                    list_of_files.append(InputMediaPhoto(media=menu_page))
                else:
                    list_of_files.append(InputMediaPhoto(media=menu_page,
                                                         caption=f"Меню на {config['date'].strftime(r'%d.%m.%Y')}"))

        # Если нужно отправить новое сообщение с одним файлом, составляем список из файлов без обработки
        elif config["new_message"]:
            for menu_page in menu_pages:
                list_of_files.append(menu_page)
        # Если нужно изменить существующее сообщение с одним файлом, составляем список из файлов,
        # Обработанных с помощью InputMediaPhoto
        else:
            for menu_page in menu_pages:
                list_of_files.append(InputMediaPhoto(media=menu_page))

        config["number_of_pages"] = len(list_of_files)

        return list_of_files, config


async def download_cleaning(result, config):
    delete_menu(config["date"])

    if config["media_group"]:
        sent_files = ""
        for i in range(0, config["number_of_pages"]):
            sent_files = sent_files + str(result[i].photo[-1].file_id) + " "
        id_string = sent_files.strip()

        await add_menu_id(config["date"], id_string)
    else:
        print()
        # Сообщение админу о том, что пользователь загрузил меню, которого нет в БД
