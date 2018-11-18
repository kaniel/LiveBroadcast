# -*- coding: utf-8 -*-

from flask.ext.script import Manager
from live import create_app
from settings import DEV
from live.models import Roles
from flask_security.utils import encrypt_password
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
import json
import os
import sys
import plistlib

app = create_app(DEV)
manager = Manager(app)

migrate = Migrate(app, app.db)
manager.add_command('db', MigrateCommand)


@manager.command
def add_su():
    su_role = app.user_datastore.create_role(**Roles.SUPER_ADMIN)
    app.user_datastore.create_role(**Roles.ADMIN)
    app.user_datastore.create_role(**Roles.USER)
    su = app.user_datastore.create_user(**{
        'email': 'admin@gmail.cn',
        'password': encrypt_password('666666'),
        'name': u'超级管理员'
    })
    app.user_datastore.add_role_to_user(su, su_role)
    su.confirmed_at = datetime.utcnow()
    app.db.session.commit()


@manager.command
def init_db():
    app.db.create_all()
    add_su()

if __name__ == "__main__":
    manager.run()
