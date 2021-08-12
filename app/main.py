from downloading import Config, dt, main
from parsing import (
    CategoryParser, OfferParser,
    clear_extracted_yml_files
)
import os


archive_file = Config.GZ_FILE
current_file = os.path.join(
            Config.BASE_DIR,
            'yml_for_parsing_{}.yml'.format(
                dt.now().strftime("%m-%d-%Y_%H:%M")
            ))
updated_urls_dict = {}


def run(archive_file, yml_file, urls_dict, offers_count=1000):
    categories = CategoryParser(archive_file, yml_file)
    offers = OfferParser(archive_file, yml_file, urls_dict, offers_count)
    menu_dict = {
        1: {
            'select': 'Вывод на печать всех объектов категорий.',
            'return': 'Все объекты категорий были выведены.'
        },
        2: {
            'select': 'Вывод на печать первых тысячи объектов офферов.',
            'return': 'Первые тысяча объектов офферов были выведены на печать.'
        },
        3: {
            'select': 'Скачивание картинок первых тысячи объектов офферов,' +
            'с последующим добавлением ссылок на них в файл.',
            'return': 'Скачивание картинок первых тысячи объектов офферов,' +
            'с последующим добавлением ссылок на них в файл завершено.'
        },
        4: {
            'select': 'Очистить все файлы текущей сессии программы и выход.',
            'return': 'Очистка всех файлов текущей сессии программы...\n' +
            'Завершение программы...'
        },
        0: {
            'select': 'Выход из программы',
            'return': 'Завершение программы...'
        }
    }

    while 1:
        print('Вы находитесь в главном меню программы.\n')
        print(
            'Вам доступны следующие действия:\n',
            *('%s: %s' % (x, menu_dict[x]['select']) for x in menu_dict),
            sep='\n', end='\n')
        selected = int(input("Выберите действие...\n",))
        print(
            "Вы выбрали: {}\n".format(
                menu_dict[selected]['select']
            ) if selected in menu_dict.keys() else
            "Ошибка считывания выбранного действия...\n"
        )
        if selected == 0:
            print(menu_dict[selected]['return'])
            exit()
        elif selected == 1: categories.print_cat_objects()
        elif selected == 2: offers.print_offer_objects()
        elif selected == 3:
            images_list = offers.get_offer_img_urls()
            main(images_list, urls_dict)
            offers.rewrote_offers_images_path()
        elif selected == 4: clear_extracted_yml_files(
            Config.BASE_DIR, Config.DOWNLOADING_DIR
        )

        if selected in menu_dict.keys():
            print(menu_dict[selected]['return'])
            if selected == 4: exit()


def run_program(archive_file, yml_file, urls_dict, offers_count=1000):
    run(archive_file, yml_file, urls_dict, offers_count)


if __name__ == '__main__':
    run_program(archive_file, current_file, updated_urls_dict)
