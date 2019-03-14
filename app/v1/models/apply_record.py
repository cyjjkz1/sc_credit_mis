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

    audit_status = db.Column(db.Integer, nullable=False, default=0)
    audit_credit = db.Column(db.Integer, nullable=True)
    audit_remark = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    audit_time = db.Column(db.DateTime, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    apply_file_id = db.Column(db.Integer, db.ForeignKey('apply_file.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    audit_department_id = db.Column(db.Integer, db.ForeignKey('audit_department.id'))

    def __init__(self,
                 apply_year,
                 apply_term,
                 apply_credit,
                 apply_detail,
                 apply_remark,
                 user_id,
                 apply_file_id,
                 project_id,
                 audit_department_id,
                 audit_status=0,
                 audit_credit=0,
                 create_time=datetime.now()):
        self.apply_year = apply_year
        self.apply_term = apply_term
        self.apply_credit = apply_credit
        self.apply_detail = apply_detail
        self.apply_remark = apply_remark
        self.user_id = user_id
        self.apply_file_id = apply_file_id
        self.project_id = project_id
        self.audit_department_id = audit_department_id
        self.audit_status = audit_status
        self.audit_credit = 0
        self.create_time = create_time

    def to_dict(self, rel_query=False):
        apply_dict = {
            "apply_year": self.apply_year,
            "apply_term": self.apply_term,
            "apply_credit": self.apply_credit,
            "apply_detail": self.apply_detail,
            "apply_remark": self.apply_remark,
            "audit_credit": self.apply_credit,
            "audit_remark": self.audit_remark,
            "audit_status": self.audit_status,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S %f")
        }
        if self.audit_time:
            apply_dict = self.audit_time.strftime("%Y-%m-%d %H:%M:%S %f")
        if rel_query:
            if self.r_user:
                apply_dict['name'] = self.r_user.name
            if self.apply_file:
                apply_dict['apply_file'] = self.apply_file.name
            if self.project:
                apply_dict['project_name'] = self.project.name
                if self.project.classify:
                    apply_dict['project_classify'] = self.project.classify.name
            if self.apply_audit_department:
                apply_dict['audit_department'] = self.apply_audit_department.name
        return apply_dict

    def save(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()


class ApplyFile(db.Model):
    __tablename__ = 'apply_file'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(30), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    records = db.relationship('ApplyRecord', backref='apply_file', uselist=False)

    def __init__(self, filename, create_time=datetime.now()):
        self.filename = filename
        self.create_time = create_time

    def to_dict(self):
        col_dict = {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.strftime("%Y-%m-%d %H:%M:%S %f"),
        }
        return col_dict

    def save(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()

