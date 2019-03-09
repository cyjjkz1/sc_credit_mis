from app import db
from datetime import datetime


class ApplyRecord(db.Model):
    __tablename__ = 'apply_record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    apply_year = db.Column(db.String(10), nullable=False)
    apply_term = db.Column(db.Integer, nullable=False)
    apply_credit = db.Column(db.Integer, nullable=False)
    apply_detail = db.Column(db.String(200), nullable=False)
    apply_remark = db.Column(db.String(200), nullable=False)

    audit_credit = db.Column(db.Integer, nullable=True)
    audit_remark = db.Column(db.String(200), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    apply_file_id = db.Column(db.Integer, db.ForeignKey('apply_file.id'))
    project = db.Column(db.Integer, db.ForeignKey('project.id'))

    def __init__(self,
                 apply_year,
                 apply_term,
                 apply_credit,
                 apply_detail,
                 apply_remark,
                 audit_credit,
                 audit_remark,
                 create_time=datetime.now()):
        self.apply_year = apply_year
        self.apply_term = apply_term
        self.apply_credit = apply_credit
        self.apply_detail = apply_detail
        self.apply_remark = apply_remark

        self.audit_credit = audit_credit
        self.audit_remark = audit_remark

        self.create_time = create_time

    def to_dict(self, rel_query=False):
        red_dict = {
            "apply_year": self.apply_year,
            "apply_term": self.apply_term,
            "apply_credit": self.apply_credit,
            "apply_detail": self.apply_detail,
            "apply_remark": self.apply_remark,
            "audit_credit": self.apply_credit,
            "audit_remark": self.audit_remark,
            "create_time": self.create_time
        }
        if self.r_user:
            red_dict['name'] = self.r_user.name
        if self.apply_file:
            red_dict['apply_file'] = self.apply_file.name
        if self.project:
            red_dict['project_name'] = self.project.name

        return red_dict


class ApplyFile(db.Model):
    __tablename__ = 'apply_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    apply_record = db.relationship('ApplyRecord', backref='apply_file', lazy='dynamic', uselist=False)

    def __init__(self, name, create_time=datetime.now()):
        self.name = name
        self.create_time = create_time

    def to_dict(self):
        col_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time
        }
        return col_dict
