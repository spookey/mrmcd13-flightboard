# -.- coding: utf-8 -.-

import os, json, re
from time import time
from urllib2 import urlopen
from app import app
from loghandler import logger
from config import *

def get_json():
    if (timestamp()/60 - frab_feed_refresh_span) >= app.last_refresh:
        load_remote()
        app.last_refresh = timestamp()
        logger.info('local json file refreshed')
    return load_local()

def timestamp():
    return int(time())

def web_scrape(url):
    try:
        response = urlopen(url)
        return response.read()
    except (urllib2.HTTPError, urllib2.URLError, httplib.HTTPException, Exception) as e:
        logger.error('could not download %s ~ %s' %(url, e))

def load_remote():
    with open(local_frab_feed, 'w') as f:
        content = web_scrape(remote_frab_feed)
        if content is not None:
            try:
                f.write(content)
            except Exception as e:
                logger.error('could not save json ~ %s' %(e))
            else:
                logger.info('json file sucessfully written')
        else:
            logger.error('json scrape failed ~ %s' %(e))

def load_local(filename=local_frab_feed):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                content = f.read().decode('utf-8')
                result = json.loads(content, strict=False)
            except (ValueError, Exception) as e:
                logger.error('could not parse json file ~ %s' %(e))
            else:
                return result
    else:
        logger.info('json file %s not found' %(filename))

