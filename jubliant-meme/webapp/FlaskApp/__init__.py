#!/usr/bin/env python


import os
import ConfigParser
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from wapi import wapi 
from models import login_manager, db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


def parseConfiguration(env):
    """ Parse the config file and return the dict
    """
    settings = dict()
    config = ConfigParser.ConfigParser()
    config.optionxform = str
    configFile = os.path.join(basedir, "config/{}".format(env))
    try:
        config.read(configFile)
        for section in config.sections():
            for option in config.options(section):
                settings[option] = config.get(section, option)
    except Exception as err:
        raise Exception(err)

    return settings


def createApp(app):
    env = os.getenv('APPLICATION_ENV', 'default')
    settings = parseConfiguration(env)
    app.config.update(settings)
    app.register_blueprint(wapi)
    bootstrap = Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    migrate = Migrate(app, db)

if __name__ == "__main__":
    createApp(app)
    app.run()
