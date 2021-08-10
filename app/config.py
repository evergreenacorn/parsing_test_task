from os import path, remove, listdir
from datetime import datetime as dt
import logging


class Config:
    BASE_DIR = path.dirname(__file__)
    GZ_FILENAME = "vinted_20210809.yml.gz"
    GZ_FILE = path.join(BASE_DIR, GZ_FILENAME)
    DOWNLOADING_DIR = path.join(BASE_DIR, 'tmp', 'somedir')
    LOGGING_FILE = path.join(
        BASE_DIR,
        'logs',
        'logs_from_{}.log'.format(dt.now().strftime("%m-%d-%Y_%H-%M-%S"))
    )
    logging.basicConfig(
        filename=LOGGING_FILE, filemode='w',
        format='[%(asctime)s] %(name)s - %(levelname)s - %(message)s')