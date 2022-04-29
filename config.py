CONTAINER_NAME = None
DB_USER = None
DB_NAME = None
DUMP_FOLDER = None

try:
    from local_config import *
except ModuleNotFoundError:
    pass