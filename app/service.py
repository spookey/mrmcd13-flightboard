# -.- coding: utf-8 -.-

import os, json, re, time
from datetime import datetime, timedelta
from urllib2 import urlopen
from config import *
from jsonhandler import get_json
from loghandler import logger
from HTMLParser import HTMLParser
from re import findall

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
    logger.info('today is day %s' %(result))
    return result

def date_display():
    daynumber = current_day_number()
    if daynumber is not None:
        json = get_json()
        if json is not None:
            return 'Day %d of %d &mdash; %s' %(int(daynumber), len(json['schedule']['conference']['days'])-1, format_date(datetime_now()))
    else:
        logger.info('no conference')
        return 'No conference &mdash; %s' %(format_date(datetime.now()))

def schedule():
    def _strconv(msg):
        for e in findall('&.+?;', msg):
            unescaped = HTMLParser().unescape(e)
            msg = msg.replace(e, unescaped)
        return msg

    def _strsplit(msg, num=fb_daparture_length):
        result = _strconv(msg)
        return [result[start:start+num].lstrip().rstrip() for start in range(0, len(result), num)]

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
                            messages = _strsplit(event['title'], fb_daparture_length)
                        else:
                            messages = _strsplit(event['title'], fb_daparture_length) + _strsplit(event['subtitle'], fb_daparture_length)

                        result.append({
                            'time': {
                                'messages': [event['start']],
                                'maxLength': fb_time_length,
                            },
                            'depature': {
                                'messages': messages,
                                'maxLength': fb_daparture_length,
                            },
                            'flight': {
                                'messages': [event['id']],
                                'maxLength': fb_flight_length,
                            },
                            'gate': {
                                'messages': [event['room']],
                                'maxLength': fb_gate_length,
                            },
                        })

            result.sort(key=lambda x: x['time']['messages'])
            logger.info('schedule ready ~ got %s entries' %(len(result)))
    return result
