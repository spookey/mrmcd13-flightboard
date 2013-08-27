# -.- coding: utf-8 -.-

from flask import render_template, send_from_directory, flash, jsonify
from config import dir_static, fb_maxrows
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
    logger.info('index requested')
    return render_template('main.html',
        title = 'Up Next',
        rows = len(schedule()),
        maxrows = fb_maxrows,
    )

@app.route('/content')
def content():
    data = {}
    data['defaults'] = load_local(flightboard_defaults)
    for i, item in enumerate(schedule()):
        data['row%d' %(i)] = item
    return jsonify(data)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(dir_static, 'favicon.png',
        mimetype='image/png'
    )

@app.errorhandler(404)
def internal_error(error):
    flash('I checked twice!')
    return render_template('error.html',
        message = 'File not found'), 404

@app.errorhandler(500)
def internal_error(error):
    flash('Panic!!1!')
    return render_template('error.html',
        message = 'An unexpected error has occurred'), 500
