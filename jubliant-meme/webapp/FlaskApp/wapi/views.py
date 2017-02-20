#!/usr/bin/env python


from . import wapi
from flask_login import login_required


@wapi.route('/')
@login_required
def index():
    return 'Hello, There!!!'
