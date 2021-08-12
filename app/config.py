from os import path, remove, listdir, makedirs
from datetime import datetime as dt
import logging


class Config:
    """
    Класс, содержащий базовые настройки приложения
    """

    BASE_DIR = path.dirname(__file__)
    GZ_FILENAME = "vinted_20210809.yml.gz"
    GZ_FILE = path.join(BASE_DIR, GZ_FILENAME)
    DOWNLOADING_DIR = path.join(BASE_DIR, 'tmp', 'somedir')
    if not path.exists(DOWNLOADING_DIR):
        makedirs(DOWNLOADING_DIR)
    LOGGING_FILES_DIR = path.join(BASE_DIR, 'logs')
    if not path.exists(LOGGING_FILES_DIR):
        makedirs(LOGGING_FILES_DIR)
    LOGGING_FILE = path.join(
        LOGGING_FILES_DIR,
        'logs_from_{}.log'.format(dt.now().strftime("%m-%d-%Y_%H-%M-%S"))
    )
    logging.basicConfig(
        filename=LOGGING_FILE, filemode='w',
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s')


CONFIG = Config
