# -.- coding: utf-8 -.-

import os, json, re, time
from datetime import datetime, timedelta
from urllib2 import urlopen
from config import *
from jsonhandler import get_json

def datetime_from_date(Ymd):
    return datetime.strptime(Ymd, '%Y-%m-%d')

def datetime_from_time(HM):
    return datetime.strptime(HM, '%H:%M')

def format_date(datetimeobj):
    return datetime.strftime(datetimeobj, '%d.%m.%Y')

def format_time(datetimeobj):
    return datetime.strftime(datetimeobj, '%H:%M')

def datetime_now():
    # return datetime.now()
    return datetime.strptime('2013-09-07 13:37', '%Y-%m-%d %H:%M') #testing, uncomment for production!


def current_day_number():
    json = get_json()
    result = None
    if json is not None:
        content = json['schedule']['conference']['days']

        for data in content:
            delta = datetime_now() - datetime_from_date(data['date'])
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
    def _strsplit(msg, num=30):
        return [msg[start:start+num].lstrip().rstrip() for start in range(0, len(msg), num)]

    json = get_json()
    today = current_day_number()
    result = []

    if today is not None:
        if json is not None:
            content = json['schedule']['conference']['days'][today]['rooms']

            for rooms in content.itervalues():
                for event in rooms:
                    if datetime_from_time(event['start']) >= datetime_from_time(format_time(datetime_now())):

                        messages = []
                        if not event['subtitle']:
                            messages = _strsplit(event['title'])
                        else:
                            messages = _strsplit(event['title']) + _strsplit(event['subtitle'])

                            result.append({
                                'time': {
                                    'messages': [event['start']],
                                    'maxLength': 8,
                                },
                                'depature': {
                                    'messages': messages,
                                    'maxLength': 30,
                                },
                                'flight': {
                                    'messages': [event['id']],
                                    'maxLength': 4,
                                },
                                'gate': {
                                    'messages': [event['room']],
                                    'maxLength': 8,
                                },
                            })

            result.sort(key=lambda x: x['time']['messages'])
    return result
