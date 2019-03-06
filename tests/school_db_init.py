#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from flask_script import Command
from app.v1.models.school import College, Major


class DeleteCol(Command):
    def run(self):
        cols = College.query.all()
        for col in cols:
            db.session.delete(col)
        db.session.commit()

class DeleteMaj(Command):
    def run(self):
        majs = Major.query.all()
        for maj in majs:
            db.session.delete(maj)
        db.session.commit()

class AddCollege(Command):
    def run(self):
        col = College('经济与管理学院')
        maj1 = Major('会计学')
        maj2 = Major('财务管理')
        maj3 = Major('市场营销')
        maj4 = Major('电子商务')
        maj5 = Major('人力资源管理')
        maj6 = Major('信息管理与信息系统')
        majs = [maj1, maj2, maj3, maj4, maj5, maj6]
        col.majores = majs
        db.session.add(col)


        col2 = College('国际商学院')
        maj21 = Major('经济与金融')
        maj22 = Major('物流管理')
        majs2 = [maj21, maj22]
        col2.majores = majs2
        db.session.add(col2)


        col3 = College('人文学院')
        maj31 = Major('社会工作')
        maj32 = Major('学前教育')
        maj33 = Major('广告学')
        majs3 = [maj31, maj32, maj33]
        col3.majores = majs3
        db.session.add(col3)

        col4 = College('电子工程学院')
        maj41 = Major('电子信息工程')
        maj42 = Major('自动化')
        maj43 = Major('汽车服务工程')
        majs4 = [maj41, maj42, maj43]
        col4.majores = majs4
        db.session.add(col4)

        col5 = College('计算机学院')
        maj51 = Major('计算机科学与技术')
        maj52 = Major('数字媒体技术')
        majs5 = [maj51, maj52]
        col5.majores = majs5
        db.session.add(col5)

        col6 = College('通信工程学院')
        maj61 = Major('通信工程')
        majs6 = [maj51]
        col6.majores = majs6
        db.session.add(col6)

