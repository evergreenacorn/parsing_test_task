# from app.parsing import Parser, CategoryParser, OfferParser
from datetime import datetime as dt
from config import Config, logging
import threading
import asyncio
import requests
import time


def download_images_list(images_list, urls_dict):
    """
    Функция, загружающая, удаленную картинку по url из images_list
    и возвращающая словарь словарей {id оффера: {'file_path': локальный путь к файлу
    картинки}}
    """
    try:
        for img_dict in images_list:
            for key in img_dict:
                image_url = img_dict[key]['picture']
                r = requests.get(image_url)
                if r.status_code == 200:
                    content_ext = r.headers['content-type'].split('/')[-1]
                    imagefile_name = Config.DOWNLOADING_DIR +\
                        '/{}_{}.{}'.format(
                            key, dt.now().strftime("%m-%d-%Y_%H:%M"),
                            content_ext)
                    with open(imagefile_name, 'wb') as f:
                        f.write(r.content)
                    # print(f'Offer {key}: Image was saved!')
                    urls_dict[key] = {'file_path': imagefile_name}
                else:
                    # print(f'Offer {key}: Error! {r.status_code}')
                    logging.warning(f'Оффер {key}: Ошибка! {r.status_code}')
    except Exception as e:
        logging.warning(f'Оффер {key}: Ошибка! {e}')
    finally:
        return urls_dict


def thread(images_list, urls_dict):
    """
    Функция выполняюшая все футуры в eventloop
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
    """
    Функция формирующая 10 потоков, в каждом из котором
    выполняются все футуры в eventloop
    """
    start_time = time.time()
    print(
        "Загрузка файлов начата в {}...".format(
            dt.now().strftime("%m-%d-%Y_%H:%M")),
        end="\n")
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
    print(
        "Загрузка файлов завершена за {}...".format(
                time.time() - start_time
            ),
        end="\n")
