#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from app import db, create_app
from flask_script import Manager, Command, Server
from flask_migrate import Migrate, MigrateCommand


from tests.school_db_init import DeleteCol, DeleteMaj, AddCollege, AddProject
from tests.user_init import UserAdd, UserDelete
from app.v1 import models


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

manager = Manager(app)

migrate = Migrate(app, db)


class CreateDB(Command):
    def run(self):
        db.create_all()
        #user = models.user.User.query.filter_by(account="13500001111").first()
        #print user.session.first().session_id

# 自定义命令
manager.add_command('createdb', CreateDB)
manager.add_command('runserver', Server(host='0.0.0.0', port=9090))
manager.add_command('db', MigrateCommand)
manager.add_command('addcol', AddCollege)
manager.add_command('delcol', DeleteCol)
manager.add_command('delmaj', DeleteMaj)
manager.add_command('addpro', AddProject)
manager.add_command('adduser', UserAdd)
manager.add_command('deluser', UserDelete)

if __name__ == '__main__':
    manager.run()
