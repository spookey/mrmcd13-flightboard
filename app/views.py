# -.- coding: utf-8 -.-

from flask import render_template, send_from_directory, flash, jsonify
from config import dir_static
from service import *
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html',
        title = 'Up Next',
    )

globald = {
        'defaults': {
            'lettersSeq': ' ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.:,;#+~*?!(){}[]/\&%|<>',
            'lettersSize': [25, 34],
            'lettersImage': 'static/img/flightBoardMingrayMonoRegular.png',
            'shadingImages': ['static/img/flightBoardHigh.png', 'static/img/flightBoardShad.png'],
            'flips': [7, 14],
            # 'sequential': True,
            'speed': 150,
            'pause': 10000,
            'messages': ['void', 'null', 'false'],
        },
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
        'test': {
            'messages': ['WALD', 'MEISTER', 'LEBER', 'WURST'],
            'maxLength': 8,
        },
}

@app.route('/test')
def test():
    return render_template('test.html',
        content = get_frab_feed()
        )

@app.route('/content.json')
def content():
    d = globald
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
