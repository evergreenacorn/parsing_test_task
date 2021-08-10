from datetime import datetime
import asyncio
import shutil
import gzip
from lxml import etree
import os


BASE_DIR = os.path.dirname(__file__)
GZ_FILENAME = "vinted_20210809.yml.gz"
GZ_FILE = os.path.join(BASE_DIR, GZ_FILENAME)
current_file = None


def uzip_yml(file_in, file_out=current_file):
    """Функция извлекает файл из архива"""
    with gzip.open(GZ_FILE, 'rb') as f_in:
        global current_file
        current_file = os.path.join(BASE_DIR, 'yml_for_parsing_{}.yml'.format(str(datetime.now())))
        with open(file_out, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_document_from_file():
    try:
        root = etree.parse(current_file).getroot()
        # return etree.tostring(root, pretty_print=True)
        return [[e.tag for e in shop] for shop in root][0]

        # tree = etree.parse(current_file).getroot()
        # lol_tree = etree.tostring(tree)
        # with open(os.path.join(
        #     BASE_DIR, 'lol_kek_{}.{}'.format("123", 'txt')), "w"
        # ) as kek_f:
        #     kek_f.writelines(str(lol_tree))
    except Exception as e:
        raise e


def _add_offer_img_local_path(element, attr, path):
    """Присваение офферу нового атрибута, содержащего локальный путь
    """
    element.set(attr, path)


"""Первые строки файла
b'<yml_catalog date="2021-02-10 09:26">\n
<shop code="vinted">\n    
<name>Vinted</name>\n    
<company>Vinted</company>\n    
<url>https://www.vinted.com/</url>\n    
<currencies>\n        
    <currency id="USD" rate="1"/>\n    
</currencies>\n    
<categories>\n        \n        
    <category id="5" parentId="" slug="men" gender="men">Men</category>\n        
    <category id="82" parentId="5" slug="accessories" gender="men">Accessories</category>\n        
</categories>
<offers>
    <offer id="28723358" group_id="28723358" available="true">
        <url>https://www.vinted.com/men/holdalls/28723358-cat-bag</url>
        <price>5.0</price>
        <currencyId>USD</currencyId>
        <categoryId>1798</categoryId>
        <picture>https://images.vinted.net/thumbs/02_00d19_NB7WTT2LWpZa5e2Pj7w4JW2R.jpeg?1612068679-4bc90409b3a1b084ae955fc51fee4c7a268ec6e3</picture>
        <vendor>UNKNOWN</vendor>
        <model>vinted-28723358</model>
        <param name="gender">men</param>
        <param name="color">Black</param>
        <name>Cat bag</name>
        <param name="size"></param>
    </offer>
    <offer id="28721192" group_id="28721192" available="true">
        <url>https://www.vinted.com/men/holdalls/28721192-guess-factory-bag</url>
        <price>14.0</price>
        <currencyId>USD</currencyId>
        <categoryId>1798</categoryId>
        <picture>https://images.vinted.net/thumbs/02_01ed8_Nj45iGP7V9AoMiaTpQnX3mWU.jpeg?1612044608-0da287f5ce60b02ea0fc350f3f992043651e9ded</picture>
        <vendor>guess factory</vendor>
        <model>vinted-28721192</model>
        <param name="gender">men</param>
        <param name="color">Black</param>
        <name>Guess factory bag</name>
        <param name="size"></param>
    </offer>
"""


if __name__ == '__main__':
    unzipped_file = uzip_yml(GZ_FILE)
    my_file = get_document_from_file()

    # from pprint import pprint
    # pprint(my_file)

    print(my_file)

    # print(dir(my_file))
