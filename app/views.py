# -.- coding: utf-8 -.-

from flask import render_template, send_from_directory, flash, jsonify
from config import dir_static
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html',
        title = 'Up Next',
    )

@app.route('/content.json')
def content():
    d = {
        'defaults': {
            'lettersSeq': ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
            'lettersSize': [25, 34],
            'lettersImage': 'static/img/flightBoardSourceCodePro.png',
            'shadingImages': ['static/img/flightBoardHigh.png', 'static/img/flightBoardShad.png'],
            'flips': [3, 7],
            'speed': 250,
            'pause': 5000,
            'messages': ['VOID', 'NULL', 'FALSE']
        },
        'test': {
            'maxLength': 8,
            'messages': ['WALD', 'MEISTER'],
        },
    }
    return jsonify(d)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(dir_static, 'favicon.png',
        mimetype='image/png'
    )

@app.errorhandler(404)
def internal_error(error):
    flash('I checked twice!')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
