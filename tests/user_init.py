#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.v1.models.user import User
from app.v1.models.school import College, Major
from flask_script import Command
from app import db
import hashlib


def md5(text):
    m = hashlib.md5()
    m = m.update(text.encode('UTF-8'))
    return m.hexdigest()


class UserAdd(Command):
    def run(self):
        user = User(name='黄二蛋', password=md5('123456'), stu_num='13541134276', role='2', class_name='2020级3班')
        col = College.query.filter_by(name='计算机学院').first()
        maj = Major.query.filter_by(name='计算机科学与技术').first()
        user.college = col
        user.major = maj
        db.session.add(user)
        db.session.commit()




