import logging.config
from os import path

log_file_config = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_config)
logger = logging.getLogger('terminal')
