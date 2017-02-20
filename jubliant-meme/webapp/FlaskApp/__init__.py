#!/usr/bin/env python


import os
import ConfigParser
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from wapi import wapi
from models import login_manager, db
from models.users import User

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


def make_shell_context():
    return dict(app=app, db=db, User=User)


if __name__ == "__main__":
    """ M A I N
    """
    app = Flask(__name__)
    env = os.getenv('APPLICATION_ENV', 'default')
    settings = parseConfiguration(env)
    app.config.update(settings)
    app.register_blueprint(wapi)
    manager = Manager(app)
    bootstrap = Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    migrate = Migrate(app, db)
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)
    manager.run()
