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

    users = db.relationship('User', backref='college', lazy='dynamic')

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

    users = db.relationship('User', backref='major', lazy='dynamic')

    def __init__(self, name, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time

    def to_json(self):
        maj_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }
        return maj_dict


class Classify(db.Model):
    __tablename__ = 'classify'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    projects = db.relationship('Project', backref='classify', lazy='dynamic')

    def __init__(self, name, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time

    def to_json(self):
        cate_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }
        return cate_dict


audit_project = db.Table('audit_project',
                         db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                         db.Column('department_id', db.Integer, db.ForeignKey('audit_department.id'), nullable=False),
                         db.Column('project_id', db.Integer, db.ForeignKey('project.id'), nullable=False)
                         )


class AuditDepartment(db.Model):
    __tablename__ = 'audit_department'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    ad_projects = db.relationship('Project',
                               secondary=audit_project,
                               backref=db.backref('audit_departments', lazy='dynamic'),
                               lazy='dynamic')

    users = db.relationship('User', backref='audit_department', lazy='dynamic')

    def __init__(self, name, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time

    def to_json(self, rel_query=False):
        dep_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }
        if rel_query:
            all_project = []
            if self.projects is not None:
                for pro in self.projects:
                    all_project.append(pro.to_dict())
            dep_dict['projects'] = all_project
        return dep_dict


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(16), nullable=False)
    detail = db.Column(db.String(200), nullable=False)
    max_credit = db.Column(db.Integer, nullable=False)
    min_credit = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    classify_id = db.Column(db.Integer, db.ForeignKey('classify.id'))

    def __init__(self, name, detail, max_credit, min_credit, create_time=datetime.now()):
        self.name = name
        self.detail = detail
        self.max_credit = max_credit
        self.min_credit = min_credit
        self.create_time = create_time

    def to_json(self, rel_query=False):
        pro_dict = {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            'max_credit': self.max_credit,
            'min_credit': self.min_credit,
            'create_time': self.create_time
        }
        if rel_query:
            all_department = []
            if self.audit_departments is not None:
                for dep in self.audit_departments:
                    all_department.append(dep.to_dict())
            pro_dict['audit_departments'] = all_department
        return pro_dict

