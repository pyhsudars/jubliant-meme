#!/usr/bin/env python


from . import wapi
from flask import render_template
from flask_login import login_required


@wapi.route('/')
def index():
    return render_template('index.html')

