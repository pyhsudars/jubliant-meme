#!/usr/bin/env python

from flask import url_for, redirect, flash
from flask_login import login_user, current_user, logout_user
from . import wapi
from models import db
from models.users import User
from lib.OAuth import OAuthSignIn


@wapi.route('/authorize/<provider>')
def oauth_authorize(provider):
    if current_user.is_authenticated:
        return redirect(url_for('wapi.index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@wapi.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('wapi.index'))


@wapi.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('wapi.index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('wapi.index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('wapi.index'))
