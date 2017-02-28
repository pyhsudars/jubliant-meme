#!/usr/bin/env python


import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from wapi import wapi
from models import login_manager, db
from models.users import load_user
from lib.utilis import Utilities

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


def createApp(app):
    env = os.getenv('APPLICATION_ENV', 'dev')
    handler = RotatingFileHandler(
        'app.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    iniFile = os.path.join(basedir, "config/{0}".format(env))
    settings = Utilities.parseConfiguration(iniFile)
    app.config.update(settings)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.register_blueprint(wapi)
    bootstrap = Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'index'
    login_manager.user_loader(load_user)
    migrate = Migrate(app, db)


if __name__ == "__main__":
    createApp(app)
    app.run()
