import threading
import asyncio
import requests
from parsing import (
    uzip_yml, get_document_from_file, _get_first_thousand_offer_objects,
    get_first_thousand_offer_img_urls, print_first_thousand_offer_objects,
    os, dt, pprint, clear_extracted_yml_files, print_all_cat_objects,
    rewrote_offers_images_path
)
from config import Config, logging
import time


def download_images_list(images_list, urls_dict):
    try:
        for img_dict in images_list:
            for key in img_dict:
                image_url = img_dict[key]['picture']
                r = requests.get(image_url)
                if r.status_code == 200:
                    content_ext = r.headers['content-type'].split('/')[-1]
                    imagefile_name = Config.DOWNLOADING_DIR +\
                        '/{}_{}.{}'.format(
                            key, dt.now().strftime("%m-%d-%Y_%H-%M-%S"),
                            content_ext)
                    with open(imagefile_name, 'wb') as f:
                        f.write(r.content)
                    # print(f'Offer {key}: Image was saved!')
                    urls_dict[key] = {'file_path': imagefile_name}
                else:
                    # print(f'Offer {key}: Error! {r.status_code}')
                    logging.warning(f'Offer {key}: Error! {r.status_code}')
    except Exception as e:
        logging.warning(f'Offer {key}: Error! {e}')
    finally:
        return urls_dict


def thread(images_list, urls_dict):
    """
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(do_stuff(images_list, urls_dict))
    loop.close()


async def do_stuff(images_list, urls_dict):
    """
    Асинхронная обертка для функции download_images_list
    """
    await download_images_list(images_list, urls_dict)
    # print("Stuff done", end="\n")


def main(images_list, urls_dict):
    print("Downloading start...", end="\n")
    num_threads = 10
    urls_per_thread = int(len(images_list) // num_threads)
    threads = [
        threading.Thread(
            target=thread,
            args=(images_list[
                i * urls_per_thread:(i+1) * urls_per_thread
            ],
            urls_dict)
        ) for i in range(num_threads)
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    print("Downloading done...", end="\n")


def run(filename, urls_dict):
    start_time = time.time()
    print("Started at: %s" % start_time, end="\n")

    # Извлекаем из архива файл
    filename = uzip_yml(Config.GZ_FILE)
    # Парсим yml в <lxml.ElementTree>
    read_file = get_document_from_file(filename)

    # Выводим все категории
    print_all_cat_objects(read_file)
    # # Выводим первые 1000 офферов
    print_first_thousand_offer_objects(read_file, 1000)

    offers_list = _get_first_thousand_offer_objects(read_file, 1000)
    images_list = get_first_thousand_offer_img_urls(offers_list)

    main(images_list, urls_dict)
    # print(updated_urls_dict)

    # Перезаписывам пути в файл .yml
    rewrote_offers_images_path(read_file, urls_dict, filename, 1000)

    # Удаляем все .yml файлы
    # clear_extracted_yml_files(Config.BASE_DIR)

    print('Finished at: %s' % (time.time() - start_time), end="\n")
