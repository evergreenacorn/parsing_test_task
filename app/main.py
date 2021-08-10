from datetime import datetime
from lxml import etree
from pprint import pprint
import asyncio
import shutil
import gzip
import os


BASE_DIR = os.path.dirname(__file__)
GZ_FILENAME = "vinted_20210809.yml.gz"
GZ_FILE = os.path.join(BASE_DIR, GZ_FILENAME)
current_file = None


def uzip_yml(file_in):
    """Функция извлекает файл из архива"""
    with gzip.open(GZ_FILE, 'rb') as f_in:
        global current_file
        current_file = os.path.join(BASE_DIR, 'yml_for_parsing_{}.yml'.format(str(datetime.now())))
        with open(current_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_document_from_file():
    """Функция возвращает <lxml.etree._ElementTree object>
        из прочитанного yml-файла
    """
    try:
        return etree.parse(current_file)
    except Exception as e:
        raise e


def _get_all_cat_objects(document):
    """Функция читает из объекта <lxml.etree._ElementTree object>
        и возвращает список объектов всех категорий
    """
    try:
        categories_obj = document.xpath("//*[self::categories]")[0]
        return categories_obj.getchildren()
    except Exception as e:
        raise e


def print_all_cat_objects(document):
    """Функция читает из объекта <lxml.etree._ElementTree object>
        и выводит на печать объекты всех категорий
    """
    categories_list = _get_all_cat_objects(document)
    return pprint([
        {"Category {}".format(category.attrib['id']): {
                x: y for x, y in category.items()
        }} for category in categories_list
    ])


def _get_first_thousand_offer_objects(document, count=1000):
    """Функция читает из объекта <lxml.etree._ElementTree object>
        и возвращает список объектов первых 1000 офферов
    """
    try:
        offers_obj = document.xpath("//*[self::offers]")[0]
        return offers_obj.getchildren()[:count]
    except Exception as e:
        raise e


def _get_offer_subelements(offer):
    """
    Функция возвращает список словарей дочерних элементов объекта
    {lxml.etree.Element Offer}
    """
    return {'Subelements': [
        {y.tag: y.text} for y in offer.getchildren()
    ]}


def print_first_thousand_offer_objects(document, count):
    """Функция читает из объекта <lxml.etree._ElementTree object>
        и выводит на печать объекты первых 1000 офферов
    """
    offers_list = _get_first_thousand_offer_objects(
        document, count)
    return pprint([
        {"Offer {}".format(offer.attrib['id']): [
            {'Attributes': {x: y for x, y in offer.items()}},
            _get_offer_subelements(offer)
        ]} for offer in offers_list
    ])


def download_image_from_offer_object(offer): ...


def _add_offer_img_local_path(element, attr, path):
    """Присваение офферу нового атрибута, содержащего локальный путь
    """
    element.set(attr, path)


if __name__ == '__main__':
    unzipped_file = uzip_yml(GZ_FILE)
    my_file = get_document_from_file()
    # all_categories = print_all_cat_objects(my_file)
    # first_thousand_offers = print_first_thousand_offer_objects(my_file)
    print_first_thousand_offer_objects(my_file, 10)
