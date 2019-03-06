#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from flask_script import Command
from app.v1.models.school import College, Major


class AddDB(Command):
    def run(self):
        cols = College.query.all()
        db.session.delete(cols)
        db.session.commit()



