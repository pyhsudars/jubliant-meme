#!/usr/bin/env python


from . import wapi
from flask import render_template


@wapi.route('/')
def index():
    return render_template('index.html')
