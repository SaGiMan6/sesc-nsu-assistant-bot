from aiogram.types import InputMediaPhoto, FSInputFile

from scripts.interaction_with_menu_data_base import check_menu_id, add_menu_id
from scripts.get_and_delete_menu import get_menu, delete_menu


async def preparing_menu(date, input_media):
    result: tuple = await check_menu_id(date)

    if result is None:
        need_to_download = True
    else:
        need_to_download = False

    media_group = []

    if need_to_download:
        menu_pages = get_menu(date)
    else:
        menu_pages = str(result[1]).split()

    if menu_pages is None:
        return [], False, False
    else:
        for num, menu_page in enumerate(menu_pages):
            if need_to_download:
                menu_pages[num] = FSInputFile(menu_page)

        for menu_page in menu_pages:
            media_group.append(InputMediaPhoto(media=menu_page))

            # if menu_page != menu_pages[-1]:
            #     media_group.append(InputMediaPhoto(media=menu_page))
            # else:
            #     media_group.append(InputMediaPhoto(media=menu_page, caption=f"Меню на {date.strftime(r'%d.%m.%Y')}"))

        if input_media:
            return media_group, need_to_download, True
        else:
            return menu_pages, need_to_download, True


async def download_cleaning(result, date, num):
    delete_menu(date)

    try:
        sent_files = ""
        for i in range(0, num):
            sent_files = sent_files + str(result[i].photo[-1].file_id) + " "
        id_string = sent_files.strip()

        await add_menu_id(date, id_string)
    except TypeError:
        print()
        # Сообщение админу о том, что пользователь загрузил меню, которого нет в БД
