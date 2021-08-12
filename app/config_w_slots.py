from os import path, makedirs
from datetime import datetime as dt
import logging


class Config:
    """
    Класс, содержащий базовые настройки приложения
    """

    __slots__ = (
        "BASE_DIR",
        "GZ_FILENAME",
        "GZ_FILE",
        "DOWNLOADING_DIR",
        "LOGGING_FILES_DIR",
        "LOGGING_FILE",
    )


CONFIG = Config()

CONFIG.BASE_DIR = path.dirname(__file__)
CONFIG.GZ_FILENAME = "vinted_20210809.yml.gz"
CONFIG.GZ_FILE = path.join(CONFIG.BASE_DIR, CONFIG.GZ_FILENAME)
CONFIG.DOWNLOADING_DIR = path.join(CONFIG.BASE_DIR, 'tmp', 'somedir')
CONFIG.LOGGING_FILES_DIR = path.join(CONFIG.BASE_DIR, 'logs')
CONFIG.LOGGING_FILE = path.join(
    CONFIG.LOGGING_FILES_DIR,
    'logs_from_{}.log'.format(dt.now().strftime("%m-%d-%Y_%H-%M-%S"))
)

if not path.exists(CONFIG.DOWNLOADING_DIR):
    makedirs(CONFIG.DOWNLOADING_DIR)

if not path.exists(CONFIG.LOGGING_FILES_DIR):
    makedirs(CONFIG.LOGGING_FILES_DIR)

logging.basicConfig(
    filename=CONFIG.LOGGING_FILE, filemode='w',
    format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s')

# for slot in CONFIG.__slots__:
#     print(slot)
