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

def datetime_now():
    return datetime.strptime('2013-09-06 13:37', '%Y-%m-%d %H:%M') #debug, change for production!
    # return datetime.now()

def is_it_conference():
    json = get_json()
    if json is not None:
        return (mk_datetime(json['schedule']['conference']['start']) <= datetime_now() <= mk_datetime(content['schedule']['conference']['end']))

def current_day_number():
    json = get_json()
    result = None
    if json is not None:
        content = json['schedule']['conference']['days']

        for data in content:
            delta = datetime_now() - mk_datetime(data['date'])
            if( delta >= timedelta(seconds=0) and delta <= timedelta(hours=24) ):
                result = int(data['index'])
                break
    return result

def date_display():
    daynumber = current_day_number()
    if daynumber is not None:
        json = get_json()
        if json is not None:
            return 'Day %d of %d &mdash; %s' %(int(daynumber), len(json['schedule']['conference']['days'])-1, format_date(datetime_now()))
    else:
        return 'No conference &mdash; %s' %(format_date(datetime.now()))

def schedule():
    json = get_json()
    today = current_day_number()
    result = {}

    if today is not None:
        if json is not None:
            content = json['schedule']['conference']['days'][today]['rooms']

            for rooms in content.itervalues():
                for event in rooms:
                    result[event['start']] = {
                        'time': event['start'],
                        'gate': event['room'],
                        'flight': event['id'],
                        'departure': [unicode(event['title']), unicode(event['subtitle'])],
                    }
    return result
