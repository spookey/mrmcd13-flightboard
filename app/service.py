# -.- coding: utf-8 -.-

import os, json, time
from config import *
from datetime import datetime, timedelta

def mk_datetime(Ymd):
    return datetime.strptime(Ymd, '%Y-%m-%d')

def load_json():
    if os.path.exists(frab_feed):
        with open(frab_feed, 'r') as f:
            try:
                content = json.loads(f.read())
            except (Exception, ValueError) as e:
                print 'error parsing file'
            else:
                return content

def schedule():

    content = load_json()
    result = []

    result.append(datetime.now())
    result.append('|||')

    for d in content['schedule']['conference']['days']:
        result.append(str(d['date']))
        result.append(mk_datetime(d['date']))
        result.append('-->')
        result.append(mk_datetime(d['date']) - datetime.now())
        result.append(str(mk_datetime(d['date']) - datetime.now()))
        result.append('//')

    result.append('-' * 23)
    isitconferencenow = (mk_datetime(content['schedule']['conference']['starttest']) <= datetime.now() <= mk_datetime(content['schedule']['conference']['endtest']))
    result.append('Today is conference? %s' %(isitconferencenow))

    return result
