# -.- coding: utf-8 -.-

from flask import render_template, send_from_directory, flash
from config import dir_static
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html',
        title = 'Up Next',
        inhalt = 'Hallo Welt',
    )

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
