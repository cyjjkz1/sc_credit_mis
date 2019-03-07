#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.v1.models.user import User
from app.v1.models.school import College, Major, AuditDepartment
from flask_script import Command
from app import db
import hashlib


def md5(text):
    m = hashlib.md5()
    m.update(text.encode('UTF-8'))
    return m.hexdigest()


class UserAdd(Command):
    def run(self):
        user = User(name='黄二蛋', password=md5('123456'), account='13541134276', role='2', class_name='2020级3班')
        col = College.query.filter_by(name='计算机学院').first()
        maj = Major.query.filter_by(name='计算机科学与技术').first()
        user.college = col
        user.major = maj
        db.session.add(user)
        db.session.commit()

        user = User(name='黄一蛋', password=md5('123456'), account='13500001111', role='2', class_name='2020级3班')
        col = College.query.filter_by(name='计算机学院').first()
        maj = Major.query.filter_by(name='计算机科学与技术').first()
        user.college = col
        user.major = maj
        db.session.add(user)
        db.session.commit()

        user = User(name='黄三蛋', password=md5('123456'), account='13500003333', role='2', class_name='2020级3班')
        col = College.query.filter_by(name='计算机学院').first()
        maj = Major.query.filter_by(name='计算机科学与技术').first()
        user.college = col
        user.major = maj
        db.session.add(user)
        db.session.commit()

        user = User(name='黄四蛋', password=md5('123456'), account='13500004444', role='2', class_name='2020级3班')
        col = College.query.filter_by(name='计算机学院').first()
        maj = Major.query.filter_by(name='计算机科学与技术').first()
        user.college = col
        user.major = maj
        db.session.add(user)
        db.session.commit()

        user = User(name='周老师', password=md5('123456'), account='13522220000', role='1')
        dep = AuditDepartment.query.filter_by(name='团委').first()
        user.audit_department = dep
        db.session.add(user)
        db.session.commit()

        user = User(name='何老师', password=md5('123456'), account='13522221111', role='1')
        dep = AuditDepartment.query.filter_by(name='社会科学教学部').first()
        user.audit_department = dep
        db.session.add(user)
        db.session.commit()



class UserDelete(Command):
    def run(self):
        users = User.query.all()
        for user in users:
            db.session.delete(user)
        db.session.commit()






