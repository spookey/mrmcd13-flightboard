# -.- coding: utf-8 -.-

import cookielib
import urllib2
from config import *

def get_frab_feed():
    base_url = 'https://frab.cccv.de'
    login_action = '/en/session?conference_acronym=MRMCD2013'
    feed_url = 'https://frab.cccv.de/en/MRMCD2013/public/schedule.json'

    cookie_file = 'my.cookie'
    cookiejar = cookielib.MozillaCookieJar(cookie_file)

    opener = urllib2.build_opener(
        urllib2.HTTPRedirectHandler(),
        urllib2.HTTPHandler(debuglevel=0),
        urllib2.HTTPSHandler(debuglevel=0),
        urllib2.HTTPCookieProcessor(cookiejar)
        )

    opener.addheaders = [('User-agent',
       ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_7) '
         'AppleWebKit/535.1 (KHTML, like Gecko) '
         'Chrome/13.0.782.13 Safari/535.1'))
    ]

    response = opener.open(base_url)
    cookiejar.save()

    login_data = {
        'user_email': 'notify@der-beweis.de',
        'user_password': 'pay-wrek-ib-ja-quag-fel',
    }

    login_url = base_url + login_action
    response = opener.open(login_url, login_data)

    cookiejar.save()

    response = opener.open(feed_url)

    return unicode(response.read(), 'utf-8')
