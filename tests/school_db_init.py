#!/usr/bin/env python
# -*- coding:utf-8 -*-

from app import db
from flask_script import Command
from app.v1.models.school import College, Major, Project, Classify, AuditDepartment


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
        majs6 = [maj61]
        col6.majores = majs6
        db.session.add(col6)


class AddProject(Command):
    def run(self):
        #dep1 = AuditDepartment('团委')
        #dep2 = AuditDepartment('社会科学教学部')
        #dep3 = AuditDepartment('教工会')
        dep1 = AuditDepartment.query.filter_by(name='团委').first()
        dep2 = AuditDepartment.query.filter_by(name='社会科学教学部').first()
        dep3 = AuditDepartment.query.filter_by(name='教工会').first()

        cate1 = Classify.query.filter_by(name='广播电视实践项目').first()
       # cate2 = Classify.query.filter_by(name='教师工作室').first()
       # cate3 = Classify.query.filter_by(name='社会实践活动').first()
        cate4 = Classify.query.filter_by(name='竞赛项目').first()
        #cate1 = Classify("广播电视实践项目")
        cate2 = Classify("教师工作室")
        cate3 = Classify("社会实践活动")
        #cate4 = Classify("竞赛项目")

        ######################
        #proj4 = Project("教师工作室", "在教师工作室参与教师工作等等等等等等等等等等等等等等等等等等等等等等等等等等等等", 4, 1)
        #proj4.classify = cate2
        #proj4.audit_departments = [dep1, dep2]

        #proj5 = Project("二级学院社会实践活动", "到二级学院参见社会实践活动表现积极等等等等等等等等等等等等等等等等等等", 4, 1)
        #proj5.classify = cate2
        #proj5.audit_departments = [dep2, dep3]
        #######################
        #proj6 = Project("境外游学项目", "到国外合作学校游学，其实就是去耍等等花钱等等等等等等", 3, 1)
        #proj6.classify = cate3
        #proj6.audit_departments = [dep1, dep2]
        #db.session.add(proj4)
        #db.session.add(proj5)
        #db.session.add(proj6)
        #db.session.commit()

        proj7 = Project("海外课堂", "在网上远程学习，并完成相应学时等等等等等等等等等等等等等等", 5, 1)
        proj7.classify = cate3
        proj7.audit_departments = [dep1, dep2, dep3]

        proj11 = Project("大学生艺术团", "参与艺术团工作、演出、创造、后勤等等等等等等等等等等等等等等等等", 4, 1)
        proj11.classify = cate3
        proj11.audit_departments = [dep1, dep2, dep3]

        proj8 = Project("英语角", "交流口语、学习第二外语等等等等等等等等等等等等等等", 4, 1)
        proj8.category = cate3
        proj8.audit_departments = [dep3]

        #######
        proj9 = Project("广播电视栏目主创", "拍个小电影、剧集、段子、文艺节目等等等等等等等等等等等等等等等等等等等等", 6, 2)
        proj9.classify = cate1
        proj9.audit_departments = [dep1, dep2, dep3]

        proj10 = Project("影视作品播出", "影视作品在校媒体、其他公共媒体播出等等等等等等等等等等等等等等等等", 6, 3)
        proj10.classify = cate1
        proj10.audit_departments = [dep3]

        db.session.add(proj7)
        db.session.add(proj8)
        db.session.add(proj9)
        db.session.add(proj10)
        db.session.add(proj11)
        db.session.commit()
