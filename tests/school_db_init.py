#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db, create_app
from flask_script import Manager, Command, Server
from flask_migrate import Migrate, MigrateCommand
from ..app.v1 import models


class AddDB(Command):
    def run(self):
        col_dict = models.school.College('外语学院')
        col_dict1 = models.school.College('物理学院')
        col_dict2 = models.school.College('生物科学学院')
        db.session.add(col_dict1)
        db.session.add(col_dict2)
        db.session.add(col_dict)
        db.session.commit()



