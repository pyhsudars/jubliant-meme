#!/usr/bin/env python


from flask_login import UserMixin
from . import login_manager, db


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
