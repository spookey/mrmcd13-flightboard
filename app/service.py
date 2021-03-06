# -.- coding: utf-8 -.-

import os, json, re, time
from datetime import datetime, timedelta
from urllib2 import urlopen
from config import *
from jsonhandler import get_json
from loghandler import logger
from HTMLParser import HTMLParser
from textwrap import wrap, fill

def datetime_from_date(Ymd):
    return datetime.strptime(Ymd, '%Y-%m-%d')

def datetime_from_time(HM):
    return datetime.strptime(HM, '%H:%M')

def format_date(datetimeobj):
    return datetime.strftime(datetimeobj, '%d.%m.%Y')

def format_time(datetimeobj):
    return datetime.strftime(datetimeobj, '%H:%M')

def datetime_now():
    return datetime.now()
    # return datetime.strptime('2013-09-07 13:37', '%Y-%m-%d %H:%M') #testing, uncomment for production!

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

def _strconv(msg):
    for e in re.findall('&.+?;', msg):
        unescaped = HTMLParser().unescape(e)
        msg = msg.replace(e, unescaped)
    return msg

def preroll(day, talk):
    json = get_json()
    temp = []
    result = []

    if json is not None:
        content = json['schedule']['conference']['days'][int(day)]['rooms']

        for rooms in content.itervalues():
            for event in rooms:
                temp.append(event)

        t = temp[int(talk)]
        speakers = ''
        for s in t['persons']:
            speakers += _strconv(s['full_public_name']) + ' '
        result = {
            'id': t['id'],
            'title': _strconv(t['title']),
            'subtitle': _strconv(t['subtitle']),
            'track': _strconv(t['track']),
            'speakers': speakers,
            'day': day,
            'time': t['start'],
            }

        return result

def schedule():
    json = get_json()
    today = current_day_number()
    result = []

    if today is not None:
        if json is not None:
            content = json['schedule']['conference']['days'][today]['rooms']

            for rooms in content.itervalues():
                for event in rooms:
                    if datetime_from_time(event['start']) >= datetime_from_time(format_time(datetime_now())):

                        time = [event['start'].rjust(fb_time_length)]
                        tdiff = datetime_from_time(event['start']) - datetime_from_time(format_time(datetime_now()))
                        if tdiff <= timedelta(minutes=boarding_time):
                            time.append('Boarding'.rjust(fb_time_length))
                        elif tdiff <= timedelta(hours=1):
                            minutedelta = '%02d Min' %(tdiff.seconds / 60)
                            time.append(minutedelta.rjust(fb_time_length))

                        gate = [event['room'].rjust(fb_gate_length)]
                        if '105' in event['room']:
                            gate.append('Workshop'.rjust(fb_gate_length))

                        flight = [event['id']]
                        if event['language']:
                            flight.append(event['language'].rjust(fb_flight_length))

                        depature = wrap(_strconv(event['title'].strip()), fb_daparture_length)
                        if event['subtitle']:
                            depature += wrap(_strconv(event['subtitle'].strip()), fb_daparture_length)

                        result.append({
                            'time': {
                                'messages': time,
                                'maxLength': fb_time_length,
                            },
                            'gate': {
                                'messages': gate,
                                'maxLength': fb_gate_length,
                            },
                            'flight': {
                                'messages': flight,
                                'maxLength': fb_flight_length,
                            },
                            'depature': {
                                'messages': depature,
                                'maxLength': fb_daparture_length,
                            },
                        })
            if len(result) == 0:
                logger.info('no talks for today')
                result.append({
                    'time': {
                            'messages': ['x' * fb_time_length, '-' * fb_time_length],
                            'maxLength': fb_time_length,
                        },
                        'gate': {
                            'messages': ['x' * fb_gate_length, '-' * fb_gate_length],
                            'maxLength': fb_gate_length,
                        },
                        'flight': {
                            'messages': ['x' * fb_flight_length, '-' * fb_flight_length],
                            'maxLength': fb_flight_length,
                        },
                        'depature': {
                            'messages': ['x' * fb_daparture_length, '-' * fb_daparture_length],
                            'maxLength': fb_daparture_length,
                        },
                    })
            result.sort(key=lambda x: x['time']['messages'])
            logger.info('schedule ready ~ got %s entries' %(len(result)))
    return result
