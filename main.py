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
logger.setLevel('INFO')


if __name__ == '__main__':
    dumper = DockerPostgresDumper(container_name=CONTAINER_NAME,
                                  db_name=DB_NAME,
                                  db_user=DB_USER)
    logger.info('Start dump data')
    path_to_dump = dumper.create_dump(DUMP_FOLDER)
    logger.info('Success. Dump: {}'.format(path_to_dump))
