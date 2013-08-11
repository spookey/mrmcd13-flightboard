# -.- coding: utf-8 -.-

import os, json, time
from config import *
from datetime import datetime, timedelta
from urllib2 import urlopen

def mk_datetime(Ymd):
    return datetime.strptime(Ymd, '%Y-%m-%d')

def load_local_json():
    if os.path.exists(local_frab_feed):
        with open(local_frab_feed, 'r') as f:
            return decode_json(f.read())

def load_remote_json():
    return decode_json(web_scrape(remote_frab_feed))

def web_scrape(url):
    try:
        response = urlopen(url)
        return response.read()
    except urllib2.HTTPError as e:
        logger.warning('HTTPError: %s' %(str(e.code)))
    except urllib2.URLError as e:
        logger.warning('URLError: %s' %(str(e.reason)))
    except httplib.HTTPException as e:
        logger.warning('HTTPException')
    except Exception:
        logger.warning('something happened')

def decode_json(input):
    # import demjson
    try:
        content = json.loads(input)
        # content = demjson.decode(input)
    except (ValueError) as e:
        print 'error parsing json!!1! %s' %(e)
    else:
        return content

def todayisday():
    for data in load_json()['schedule']['conference']['days']:
        if( datetime.now() - mk_datetime(data['date']) >= timedelta(seconds=0)):
            result = str(data['date']), str(data['index'])
            break;
        else:
            result = str(datetime.strftime(datetime.now(), '%Y-%m-%d')), str(-1)
    return result

def schedule():

    content = load_local_json()

    result = []

    result.append(datetime.now())
    result.append('|||')

    if content is not None:
        for d in content['schedule']['conference']['days']:
            result.append(str(d['date']))
            result.append(mk_datetime(d['date']))
            result.append('-->')
            result.append(mk_datetime(d['date']) - datetime.now())
            result.append(str(mk_datetime(d['date']) - datetime.now()))
            result.append('//')

        result.append('-' * 23)
        isitconferencenow = (mk_datetime(content['schedule']['conference']['start']) <= datetime.now() <= mk_datetime(content['schedule']['conference']['end']))
        result.append('Today is conference? %s' %(isitconferencenow))

    return result
