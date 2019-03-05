#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from app import db, create_app
from flask_script import Manager, Command, Server
from flask_migrate import Migrate, MigrateCommand


# import db model
from app.v1 import models


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

migrate = Migrate(app, db)


class CreateDB(Command):
    def run(self):
        db.create_all()


class AddDB(Command):
    def run(self):
        pass


# 自定义命令
manager.add_command('createdb', CreateDB)
manager.add_command('runserver', Server(host='0.0.0.0', port=9090))
manager.add_command('db', MigrateCommand)
manager.add_command('adddb', AddDB)


if __name__ == '__main__':
    manager.run()
