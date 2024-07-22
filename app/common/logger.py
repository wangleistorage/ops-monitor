
from logging.handlers import RotatingFileHandler
from settings import config
import logging
import os


# get logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# log formatter
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s","%Y-%m-%d %H:%M:%S")

# app handler
app_handler = RotatingFileHandler(f'{config.LOG_PATH}/app.log', maxBytes=100000000, backupCount=100)
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

# run handler
run_handler = RotatingFileHandler(f'{config.LOG_PATH}/run.log', maxBytes=100000000, backupCount=100)
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

# add handler
logger.getChild('app').addHandler(app_handler)
logger.getChild('run').addHandler(app_handler)

# get logger
app_logger = logger.getChild('app')
run_logger = logger.getChild('run')
