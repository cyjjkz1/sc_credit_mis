#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.String(10), nullable=False)
    role = db.Column(db.Integer, nullable=False) # 0 admin 1 教师  2 学生
    class_name = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now
                            )
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))

    def __init__(self, name, password, user_id, role, class_name, create_time, college_id, major_id):
        self.name = name
        self.password = password
        self.user_id = user_id
