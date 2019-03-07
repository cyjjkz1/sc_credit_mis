#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from datetime import datetime


class User(db.Model):
    """
    role  # 0 admin 1 教师  2 学生
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    stu_num = db.Column(db.String(20), nullable=False)
    role = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    college_id = db.Column(db.Integer, db.ForeignKey('college.id'))
    major_id = db.Column(db.Integer, db.ForeignKey('major.id'))

    def __init__(self, name, password, user_id, role, class_name, college_id, major_id, create_time=datetime.now()):
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
        self.user_id = user_id
        self.role = role
        self.class_name = class_name
        self.college_id = college_id
        self.major_id = major_id
        self.create_time = create_time

    def to_json(self):
        user_dict = {
            "name": self.name,
            "password": self.password,
            "user_id": self.user_id,
            "role": self.role,
            "class_name": self.class_name,
            "create_time": self.create_time,
        }
        if self.college:
            user_dict['college'] = self.college.name
        if self.major:
            user_dict['major'] = self.major.name
        return user_dict;

