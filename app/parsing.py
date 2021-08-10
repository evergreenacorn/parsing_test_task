from datetime import datetime as dt
from pprint import pprint
from config import Config
from lxml import etree
import shutil
import gzip
import os


def uzip_yml(file_in):
    """Функция извлекает файл из архива"""
    with gzip.open(Config.GZ_FILE, 'rb') as f_in:
        current_file = os.path.join(
            Config.BASE_DIR,
            'yml_for_parsing_{}.yml'.format(
                str(dt.now()))
        )
        with open(current_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    return current_file


def get_document_from_file(filename):
    """Функция возвращает <lxml.etree._ElementTree object>
        из прочитанного yml-файла
    """
    try:
        return etree.parse(filename)
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
        и возвращает список объектов первых @count офферов
    """
    try:
        offers_obj = document.xpath("//*[self::offers]/offer[@available='true']")[0].getparent()
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


def get_first_thousand_offer_img_urls(offers_list):
    """
    Функция возвращает список словарей, где:
    {'offer_id': {'picture': 'picture_url'}}
    """
    return [{offer.attrib['id']: {
        x.tag: x.text for x in offer.getchildren() if x.tag == 'picture'
    }} for offer in offers_list]


def print_first_thousand_offer_objects(document, count=1000):
    """Функция читает из объекта <lxml.etree._ElementTree object>
        и выводит на печать объекты первых @count офферов
    """
    offers_list = _get_first_thousand_offer_objects(
        document, count)
    return pprint([
        {"Offer {}".format(offer.attrib['id']): [
            {'Attributes': {x: y for x, y in offer.items()}},
            _get_offer_subelements(offer)
        ]} for offer in offers_list
    ])


def rewrote_offers_images_path(document, urls_dict, filename, count):

    offers_obj = document.xpath("//*[self::offers]/offer[@available='true']")[0].getparent()
    offers_objects = offers_obj.getchildren()[:count]
    [
        offer.set(
            'file_path', urls_dict[offer.attrib['id']]['file_path']
        ) for offer in offers_objects if offer.attrib['id'] in urls_dict
    ]
    root_tree = offers_objects[0].getroottree()
    root_tree.write(filename, pretty_print=True)


def clear_extracted_yml_files(base_dir):
    """
    Очистка директории проекта от распакованных из
    архива yml-файлов
    """
    try:
        yml_files = [
            os.path.join(base_dir, f) for f in os.listdir(base_dir) if (
                f.startswith('yml_') and os.path.isfile(
                    os.path.join(base_dir, f)
                )
            )]
        for f in yml_files:
            os.remove(f)
            print(f'File {f} was successfully removed!', end='\n')
    except Exception as e:
        raise e
