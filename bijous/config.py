# coding=utf-8
import logging
import os
import sys

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = os.path.join(ROOT_PATH, 'data')

EN_DICT_PATH = os.path.join(DATA_PATH, 'en_vocab.txt')

# Logger Config
LOG_LEVEL = os.getenv('BIROUS_LOG_LEVEL', 'INFO')
logger = logging.getLogger('bijous')

if LOG_LEVEL == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s')
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)
logger.propagate = False
