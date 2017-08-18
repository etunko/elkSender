import logging
import logging.handlers
import os


def importantLog(logger, mess):
    logger("***************************************************")
    logger("***************************************************")
    logger(mess)
    logger("***************************************************")
    logger("***************************************************")


log_file = 'log.log'
log_file_size = 10*1000**2
logger = logging.getLogger(os.getcwd())
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
fh = logging.handlers.RotatingFileHandler(log_file, maxBytes=log_file_size, backupCount=5)
fh.setFormatter(formatter)
logger.addHandler(fh)
