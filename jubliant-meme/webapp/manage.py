#!/usr/bin/env python

import os
import sys
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


def make_shell_context():
    return dict(app=app, db=db, User=User)

def manage(app):
    createApp(app)
    manager = Manager(app)
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)
    manager.run()

if __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'FlaskApp')))
    from FlaskApp import app, createApp
    manage(app)
