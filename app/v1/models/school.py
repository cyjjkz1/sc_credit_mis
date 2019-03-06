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


class AuditDepartment(db.Model):
    __table__ = 'audit_department'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    projects = db.relationship('Project', backref='audit_department', lazy='dynamic')


class Category(db.Model):
    __table__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    projects = db.relationship('Project', backref='category', lazy='dynamic')


class Project(db.Model):
    __table__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    max_credit = db.Column(db.Integer, nullable=False)
    min_credit = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('audit_department.id'))
