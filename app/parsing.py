from pprint import pprint
from lxml import etree
import shutil
import gzip
import os


class Parser:
    """
    Базовый класс парсера, реализующий методы распаковки архива
    и объявления переменной document(<lxml.etree._ElementTree object>)
    экземпляра
    """

    def __init__(self, archive_file, yml_file):
        self.archive_file = archive_file
        self.yml_file = yml_file
        self.document = self.__get_document_from_file()

    def __uzip_yml(self, archive_file, yml_file):
        """Функция извлекает файл из архива"""
        try:
            with gzip.open(archive_file, 'rb') as f_in:
                with open(yml_file, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            raise e

    def __get_document_from_file(self):
        """Функция возвращает <lxml.etree._ElementTree object>
            из прочитанного yml-файла
        """
        self.__uzip_yml(self.archive_file, self.yml_file)
        try:
            if os.path.isfile(self.yml_file):
                return etree.parse(self.yml_file)
            else:
                raise FileNotFoundError
        except Exception as e:
            raise e


class CategoryParser(Parser):
    """
    Класс, содержащий методы для работы с информацией объектов Category
    """

    def __init__(self, archive_file, yml_file):
        super().__init__(archive_file, yml_file)

    def __get__cat_objects(self):
        """Функция читает из объекта <lxml.etree._ElementTree object>
            и возвращает список объектов всех категорий
        """
        try:
            categories_obj = self.document.xpath("//*[self::categories]")[0]
            return categories_obj.getchildren()
        except Exception as e:
            raise e

    def print_cat_objects(self):
        """Функция читает из объекта <lxml.etree._ElementTree object>
            и выводит на печать объекты всех категорий
        """
        categories_list = self.__get__cat_objects()
        return pprint([
            {"Category {}".format(category.attrib['id']): {
                    x: y for x, y in category.items()
            }} for category in categories_list
        ])


class OfferParser(Parser):
    """Класс, содержащий методы для работы с информацией объектов Offer"""

    def __init__(self, archive_file, yml_file, urls_dict, count=1000):
        super().__init__(archive_file, yml_file)
        self.urls_dict = urls_dict
        self.count = count

    def __get_offer_objects(self):
        """Функция читает из объекта <lxml.etree._ElementTree object>
            и возвращает список объектов первых @count офферов
        """
        try:
            offers_obj = self.document.xpath(
                "//*[self::offers]/offer[@available='true']"
            )[0].getparent()
            return offers_obj.getchildren()[:self.count]
        except Exception as e:
            raise e

    def __get_offer_subelements(self, offer):
        """
        Функция возвращает список словарей дочерних элементов объекта
        {lxml.etree.Element Offer}
        """
        return {'Subelements': [
            {y.tag: y.text} for y in offer.getchildren()
        ]}

    def get_offer_img_urls(self):
        """
        Функция возвращает список словарей, где:
        {'offer_id': {'picture': 'picture_url'}}
        """
        offers_list = self.__get_offer_objects()
        return [{offer.attrib['id']: {
            x.tag: x.text for x in offer.getchildren() if x.tag == 'picture'
        }} for offer in offers_list]

    def print_offer_objects(self):
        """Функция читает из объекта <lxml.etree._ElementTree object>
            и выводит на печать объекты первых @count офферов
        """
        offers_list = self.__get_offer_objects()
        return pprint([
            {"Offer {}".format(offer.attrib['id']): [
                {'Attributes': {x: y for x, y in offer.items()}},
                self.__get_offer_subelements(offer)
            ]} for offer in offers_list
        ])

    def rewrote_offers_images_path(self):
        offers_objects = self.__get_offer_objects()
        [
            offer.set(
                'file_path', self.urls_dict[offer.attrib['id']]['file_path']
            ) for offer in offers_objects if offer.attrib[
                'id'] in self.urls_dict
        ]
        root_tree = offers_objects[0].getroottree()
        root_tree.write(self.yml_file, pretty_print=True)


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
    except Exception as e:
        raise e
