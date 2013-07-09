# -.- coding: utf-8 -.-

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('main.html',
        title = 'Up Next',
        inhalt = 'Hallo Welt',
    )
