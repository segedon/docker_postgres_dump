"""
In home directory in container create file .pgpass
Add info about DB_USER:
hostname:port:database:username:password
"""
import logging

from dumper import DockerPostgresDumper
from config import *


logger = logging.getLogger()
logger.addHandler(logging.StreamHandler())
file_handler = logging.FileHandler('dump.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
logger.addHandler(file_handler)
logger.setLevel('INFO')


if __name__ == '__main__':
    dumper = DockerPostgresDumper(container_name=CONTAINER_NAME,
                                  db_name=DB_NAME,
                                  db_user=DB_USER)
    logger.info('Start dump data')
    try:
        path_to_dump = dumper.create_dump(DUMP_FOLDER)
    except Exception as e:
        logger.exception('Error: {}'.format(e))
    else:
        logger.info('Success. Dump: {}'.format(path_to_dump))
