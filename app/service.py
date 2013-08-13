# -.- coding: utf-8 -.-

import os, json, re, time
from datetime import datetime, timedelta
from urllib2 import urlopen
from config import *
from jsonhandler import get_json

def mk_datetime(Ymd):
    return datetime.strptime(Ymd, '%Y-%m-%d')

def format_date(datetimeobj):
    return datetime.strftime(datetimeobj, '%d.%m.%Y')

def get_day_number():
    json = get_json()
    content = None
    if json is not None:
        content = json['schedule']['conference']['days']

        def _fmt(today=datetime.now(), curday='-1', lastday=content[-1]['index']):
            return '%s of %s' %(curday, lastday), format_date(today)

        for data in content:
            if( datetime.now() - mk_datetime(data['date']) >= timedelta(seconds=0)):
                result = _fmt(mk_datetime(data['date']), data['index'])
                break;
            else:
                result = _fmt(lastday='-1')
        return result

    return content

def is_it_conference():
    json = get_json()
    if json is not None:
        return (mk_datetime(json['schedule']['conference']['start']) <= datetime.now() <= mk_datetime(content['schedule']['conference']['end']))

def schedule():
    json =  get_json()
    content = None
    if json is not None:
        content = json['schedule']['conference']['days']

    result = []

    result.append(datetime.now())
    result.append('|||')

    if content is not None:
        for d in content:
            result.append(str(d['date']))
            result.append(mk_datetime(d['date']))
            result.append('-->')
            result.append(mk_datetime(d['date']) - datetime.now())
            result.append(str(mk_datetime(d['date']) - datetime.now()))
            result.append('//')

    result.append('-' * 23)
    result.append('Today is conference? %s' %(is_it_conference()))

    return result
