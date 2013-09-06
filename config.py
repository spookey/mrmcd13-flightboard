# -.- coding: utf-8 -.-

# folders
import os
basedir = os.path.abspath(os.path.dirname(__file__))
dir_static = os.path.join(basedir, 'app/static')

# json feeds
remote_frab_feed = 'https://frab.cccv.de/en/MRMCD2013/public/schedule.json'
# the remote feed gets cached there:
local_frab_feed = os.path.join(basedir, 'schedule.json')
# the cache is refreshed every x minutes:
frab_feed_refresh_span = 15

# logging
logfile = os.path.join(basedir, 'up_next.log')

# flightboard configuration
flightboard_defaults = os.path.join(basedir, 'app/flightboard_defaults.json')
fb_maxrows = 16
fb_rowupdate = 3000
fb_json_reload = 60000
fb_pagerefresh = 23000

# flightboard character width
fb_time_length = 8
fb_gate_length = 8
fb_flight_length = 4
fb_daparture_length = 30

# show 'Boarding' n minutes before start
boarding_time = 15

#>>> import os
#>>> os.urandom(24)
SECRET_KEY = 'Blafasellaberblubbdozier'

