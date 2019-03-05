#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime


class College(db.Model):
    __tablename__ = 'college'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    majores = db.relationship('Major', backref='college', lazy='dynamic')

    def __init__(self, name, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time

    def to_dict(self, rel_query=False):
        col_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }
        if rel_query:
            all_major = []
            if self.majores is not None:
                for maj in self.majores:
                    all_major.append(maj.to_dict())
            col_dict['majores'] = all_major

        return col_dict


class Major(db.Model):
    __tablename__ = 'major'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))

    def __init__(self, name, college_id, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time
        self.college_id = college_id

    def to_json(self):
        maj_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }
        return maj_dict