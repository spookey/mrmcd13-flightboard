# -.- coding: utf-8 -.-

from flask import render_template, send_from_directory, flash, jsonify
from config import dir_static
from loghandler import logger
from jsonhandler import load_local
from service import *
from app import app

servicefunctions = {
            'get_day_number': get_day_number(),
        }
app.jinja_env.globals.update(servicefunctions = servicefunctions)

@app.route('/')
@app.route('/index')
def index():
    logger.info('index requested')
    return render_template('main.html',
        title = 'Up Next',
    )

globald = {
        'time': {
            'messages': ['23:42'],
            'maxLength': 8,
        },
        'depature': {
            'messages': ['Biertrinken gegen den Krieg', 'Praktizierter Pazifismus'],
            'maxLength': 30,
        },
        'flight': {
            'messages': ['2342'],
            'maxLength': 4,
        },
        'gate': {
            'messages': ['Saal 23', '5. Stock'],
            'maxLength': 8,
        },
}

@app.route('/test')
def test():
    return render_template('test.html',
        content = schedule(),
        )

@app.route('/content')
def content():
    globald.update(load_local(flightboard_defaults))
    return jsonify(globald)

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
    return render_template('error.html',
        message = 'An unexpected error has occurred'), 500
