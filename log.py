import logging
from logging.handlers import RotatingFileHandler
import configparser
import os

def log():
    dirname = os.path.dirname(__file__)
    configFile = os.path.join(dirname, 'config.ini')
    logFile = os.path.join(dirname, 'qradar.log')

    config = configparser.ConfigParser()
    config.read(configFile)
    
    logger = logging.getLogger('qradar-qid')

    #Create handler
    file_handler = RotatingFileHandler(logFile, maxBytes=100000, backupCount=5, mode='a')

    #Set format
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
    file_handler.setFormatter(file_format)
    if not logger.handlers:
        logger.addHandler(file_handler)
    logger.setLevel(level=config['log']['logLevel'])

    return logger