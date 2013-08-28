# -.- coding: utf-8 -.-

# folders
import os
basedir = os.path.abspath(os.path.dirname(__file__))
dir_static = os.path.join(basedir, 'app/static')

# feeds
remote_frab_feed = 'https://frab.cccv.de/en/MRMCD2013/public/schedule.json'
# the remote feed gets cached there:
local_frab_feed = os.path.join(basedir, 'schedule.json')
# the cache is refreshed every x minutes:
frab_feed_refresh_span = 15

# logs
logfile = os.path.join(basedir, 'up_next.log')

# flightboard
flightboard_defaults = os.path.join(basedir, 'app/flightboard_defaults.json')
fb_maxrows = 16
fb_rowupdate = 2000
fb_time_length = 8
fb_daparture_length = 30
fb_flight_length = 4
fb_gate_length = 8

#>>> import os
#>>> os.urandom(24)
SECRET_KEY = 'Blafasellaberblubbdozier'

