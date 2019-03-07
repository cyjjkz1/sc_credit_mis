#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.v1.models.user import User
from flask_script import Command
from app import db
import hashlib

def md5(text):
    m = hashlib.md5()
    m = m.update(text.encode('UTF-8'))
    return m.hexdigest()

class UserAdd(Command):
    def run(self):
        user = User(name='黄二蛋', password=md5('123456'), user_id='13541134276', '2', '2020级3班', 1, 1)


