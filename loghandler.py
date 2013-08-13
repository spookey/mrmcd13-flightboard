# -.- coding: utf-8 -.-

from config import logfile
from logging import getLogger, Formatter, INFO
from logging.handlers import RotatingFileHandler

filehandler = RotatingFileHandler(logfile, 'a', 1 * 1024 * 1024, 5)
filehandler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(module)s.%(funcName)s:%(lineno)d]'))

logger = getLogger('up_next')
logger.setLevel(INFO)
logger.addHandler(filehandler)
