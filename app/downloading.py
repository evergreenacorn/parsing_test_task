import asyncio
import requests
from parsing import (
    uzip_yml, get_document_from_file, _get_first_thousand_offer_objects,
    get_first_thousand_offer_img_urls, print_first_thousand_offer_objects,
    os, dt, pprint, clear_extracted_yml_files
)
from config import Config, logging


def download_images_list(images_list):
    for img_dict in images_list:
        for key in img_dict:
            image_url = img_dict[key]['picture']
            r = requests.get(image_url)
            if r.status_code == 200:
                content_ext = r.headers['content-type'].split('/')[-1]
                with open(
                    Config.DOWNLOADING_DIR + '/{}_{}.{}'.format(
                        key,
                        dt.now().strftime("%m-%d-%Y_%H-%M-%S"),
                        content_ext
                        ),
                    'wb') as f:
                    f.write(r.content)
                    print(f'Offer {key}: Image was saved!')
            else:
                print(f'Offer {key}: Error! {r.status_code}')
                logging.warning(f'Offer {key}: Error! {r.status_code}')


def run():
    uzip_yml(Config.GZ_FILE)
    my_file = get_document_from_file()
    # all_categories = print_all_cat_objects(my_file)
    # first_thousand_offers = print_first_thousand_offer_objects(my_file)

    # print_first_thousand_offer_objects(my_file, 10)

    offers_list = _get_first_thousand_offer_objects(my_file, count=100)
    images_list = get_first_thousand_offer_img_urls(offers_list)
    downloading = download_images_list(images_list)
    print(downloading)
    clear_extracted_yml_files(Config.BASE_DIR)


if __name__ == '__main__':
    run()
