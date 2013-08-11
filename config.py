# -.- coding: utf-8 -.-

import os
basedir = os.path.abspath(os.path.dirname(__file__))
dir_static = os.path.join(basedir, 'app/static')

local_frab_feed = os.path.join(basedir, 'schedule_linted.json')
remote_frab_feed = 'https://frab.cccv.de/en/MRMCD2013/public/schedule.json'

#>>> import os
#>>> os.urandom(24)
SECRET_KEY = 'Blafasellaberblubbdozier'
