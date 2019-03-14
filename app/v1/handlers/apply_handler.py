#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from flask_restful import Resource
from ..models.apply_record import ApplyRecord
from flask import current_app as app
from flask import jsonify, make_response, request
from base_handler import with_credit_user, BaseHandler, HandlerException
from data_packer import RequiredField, OptionalField, converter, SelectorField
from data_packer.checker import (
    ReChecker, LenChecker
)
from app import db
from ..constant import RESP_CODE
POST_year = RequiredField('apply_year', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9~]{1,20}'))
POST_credit = RequiredField('apply_credit', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1}'))
POST_term = RequiredField('apply_term', converter=converter.TypeConverter(str), checker=ReChecker(r'[12]{1}'))
POST_detail = RequiredField('apply_detail', converter=converter.TypeConverter(str),
                            checker=LenChecker(max_len=200, min_len=20))
POST_apply_remark = RequiredField('apply_remark',
                                  converter=converter.TypeConverter(str),
                                  checker=LenChecker(max_len=200, min_len=0))
POST_user_id = RequiredField('user_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))
POST_file_id = RequiredField('apply_file_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))
POST_project_id = RequiredField('project_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))
POST_audit_department_id = RequiredField('audit_department_id',
                                         converter=converter.TypeConverter(str),
                                         checker=ReChecker(r'[0-9]{1,}'))

GET_record_id = RequiredField('id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))

OPTION_year = OptionalField(src_name='apply_year',
                            converter=converter.TypeConverter(str),
                            checker=ReChecker(r'[0-9~]{1,20}'))

OPTION_term = OptionalField(src_name='apply_term',
                            converter=converter.TypeConverter(str),
                            checker=ReChecker(r'[12]{1}'))

OPTION_status = OptionalField(src_name='audit_status',
                              converter=converter.TypeConverter(str),
                              checker=ReChecker(r'[01]{1}'))


class ApplyHandler(BaseHandler):
    POST_FIELDS = [
        POST_year, POST_credit, POST_term,
        POST_detail, POST_apply_remark,
        POST_user_id, POST_file_id,
        POST_project_id, POST_audit_department_id
    ]
    GET_FIELDS = [GET_record_id]
    session_id = None

    def get(self):
        get_ret = self.handle()
        return jsonify(get_ret)

    def post(self):
        ret = self.handle()
        resp = make_response(jsonify(ret), 200)
        if self.session_id:
            app.logger.info('sessionid={}'.format(self.session_id))
            resp.set_cookie('sessionid', self.session_id)
        return resp

    @with_credit_user
    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        app.logger.info('func=parse_request_params | parse_params = {} '.format(params))

        try:
            if request.method == 'POST':
                user = self.credit_user
                userid = str(user.id)
                if userid == params['user_id']:
                    record = ApplyRecord(params['apply_year'],
                                         params['apply_term'],
                                         params['apply_credit'],
                                         params['apply_detail'],
                                         params['apply_remark'],
                                         params['user_id'],
                                         params['apply_file_id'],
                                         params['project_id'],
                                         params['audit_department_id']
                                         )
                    record.save()
                    return {'recod_id': str(record.id)}
                else:
                    raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='用户身份有误, 请重新登录')
            else:
                record = ApplyRecord.query.filter_by(**params).first()
                if record:
                    return record.to_dict(rel_query=True)
                else:
                    return {}
        except BaseException as e:
            db.session.rollback()
            raise e


class RecordListHandler(BaseHandler):
    GET_FIELDS = [SelectorField(
        fields=[
            OPTION_year,
            OPTION_term,
            OPTION_status
        ]
    )]

    def get(self):
        get_ret = self.handle()
        return jsonify(get_ret)

    @with_credit_user
    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        app.logger.info('func=parse_request_params | parse_type={} | parse_params = {}'.format(type(params), params))
        params['user_id'] = self.credit_user.id
        try:
            records = ApplyRecord.query.filter_by(**params).all()
            temp_re_list = []
            if records:
                for record in records:
                    temp_re_list.append(record.to_dict(rel_query=True))
            return temp_re_list
        except BaseException as e:
            db.session.rollback()
            raise e


class DepartmentRecordsHandler(BaseHandler):
    def get(self):
        get_ret = self.handle()
        return jsonify(get_ret)

    def _handle(self, *args, **kwargs):
        try:
            user = self.credit_user
            department = user.apply_audit_department
            records = department.records
            temp_re_list = []
            if records:
                for record in records:
                    temp_re_list.append(record.to_dict(rel_query=True))
            return temp_re_list
        except BaseException as e:
            db.session.rollback()
            raise e


class AuditApplyRecordHandler(BaseHandler):
    def post(self):
        ret = self.handle()
        resp = make_response(jsonify(ret), 200)
        if self.session_id:
            app.logger.info('sessionid={}'.format(self.session_id))
            resp.set_cookie('sessionid', self.session_id)
        return resp

    @with_credit_user
    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        app.logger.info('func=parse_request_params | parse_params = {} '.format(params))

        try:
            pass
        except BaseException as e:
            db.session.rollback()
            raise e