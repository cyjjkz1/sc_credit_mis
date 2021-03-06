#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime


class Session(db.Model):
    __tablename__ = 'session'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(60), nullable=False)
    expire = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, session_id, expire=3, create_time=datetime.now()):
        self.session_id = session_id
        self.expire = expire
        self.create_time = create_time

    def to_dict(self):
        cookie_dict = {
            'sessionid': self.session_id,
            'expire': self.expire,
            'create_time': self.create_time.strftime("%Y-%m-%d %H:%M:%S %f")
        }
        return cookie_dict

    def save(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()


class User(db.Model):
    """
    role  # 0 admin 1 教师  2 学生
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    account = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(10), nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('audit_department.id'))

    session = db.relationship('Session', backref='user', uselist=False)
    apply_records = db.relationship('ApplyRecord', backref='r_user', lazy='dynamic')

    def __init__(self, name, password, account, role, class_name="未知", create_time=datetime.now()):
        """
        :param name: 用户姓名
        :param password: 加密后存md5
        :param user_id: admin: 000000    教师: 职工号    学生: 学号
        :param role: 角色 0 admin   1 教师     2 学生
        :param class_name: 班级名称
        :param create_time: 入学时间
        :param college_id: 学院表中的id
        :param major_id: 专业id
        """
        self.name = name
        self.password = password
        self.account = account
        self.role = role
        self.class_name = class_name
        self.create_time = create_time

    def to_dict(self):
        user_dict = {
            "user_id": self.id,
            "name": self.name,
            "account": self.account,
            "role": self.role,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S %f"),
        }
        if self.role == 1:
            # 老师
            if self.audit_department:
                user_dict["department"] = self.audit_department.name
        elif self.role == 2:
            # 学生
            user_dict['class_name'] = self.class_name
            if self.college:
                user_dict['college'] = self.college.name
            if self.major:
                user_dict['major'] = self.major.name
        else:
            # admin
            pass
        return user_dict

    def save(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

