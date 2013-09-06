# -.- coding: utf-8 -.-

from flask import render_template, send_from_directory, flash, jsonify
from config import dir_static, fb_maxrows, no_talks
from loghandler import logger
from jsonhandler import load_local
from service import *
from app import app

servicefunctions = {
            'date_display': date_display(),
        }
app.jinja_env.globals.update(servicefunctions = servicefunctions)

@app.route('/')
@app.route('/index')
def index():
    blocklog('index requested')
    rows = len(schedule())
    print 'r', rows
    if rows == 0:
        rows += 1;
        print 'rows', rows
    return render_template('main.html',
        title = 'Up Next',
        rows = rows,
        maxrows = fb_maxrows,
        rowupdate = fb_rowupdate,
        jsonreload = fb_json_reload,
        pagerefresh = fb_pagerefresh,
    )

@app.route('/content')
def content():
    blocklog('content requested')
    data = {}
    data['defaults'] = load_local(flightboard_defaults)
    for i, item in enumerate(schedule()):
        data['row%d' %(i)] = item
    if len(data) == 1:
        data['row0'] = load_local(no_talks)

    return jsonify(data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(dir_static, 'favicon.png',
        mimetype='image/png'
    )

@app.errorhandler(404)
def internal_error(error):
    logger.error('Request Error: %s' %(error))
    flash('I checked twice!')
    return render_template('error.html',
        message = 'File not found'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error('Request Error: %s' %(error))
    flash('Panic!!1!')
    return render_template('error.html',
        message = 'An unexpected error has occurred'), 500

def blocklog(msg, char='-'):
    logger.info(char * len(msg))
    logger.info(msg)
    logger.info(char * len(msg))
