# -.- coding: utf-8 -.-

from flask import render_template, flash
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html',
        title = 'Up Next',
        inhalt = 'Hallo Welt',
    )

@app.errorhandler(404)
def internal_error(error):
    flash('I checked twice!')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
