# -.- coding: utf-8 -.-

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

# log flask messages too
if app.debug is not True:
    from loghandler import filehandler
    app.logger.addHandler(filehandler)
    logger = app.logger

logger.info('startup')
logger.info('-' * 7)

# initialize refresh cycle
app.last_refresh = 0

# do the magic
from app import views
