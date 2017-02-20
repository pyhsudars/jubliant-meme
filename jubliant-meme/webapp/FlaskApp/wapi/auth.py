#!/usr/bin/env python

from flask import request
from flask_login import login_user
from . import wapi
from models.users import User


@wapi.route('/login/', methods=['GET', 'POST'])
def login():
    if request.authorization:
        user = request.authorization.get('username', None)
        username = User.query.filter_by(username=user).first()
        if username is not None and \
            username.verify_password(
                request.authorization.get('password', None)
                ):
            login_user(username)
            return "Hello {}".format(username.username)
    return request.data
