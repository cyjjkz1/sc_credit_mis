#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from flask_restful import Resource
from ..models.apply_record import ApplyRecord
from flask import current_app as app
from flask import jsonify, make_response
from base_handler import with_credit_user, BaseHandler, HandlerException
from data_packer import RequiredField, converter
from data_packer.checker import (
    ReChecker, LenChecker
)
from app import db
from ..constant import RESP_CODE
POST_year = RequiredField('apply_year', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9~]{1,20}'))
POST_credit = RequiredField('apply_credit', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1}'))
POST_term = RequiredField('apply_term', converter=converter.TypeConverter(str), checker=LenChecker(r'[12]{1}'))
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


class ApplyHandler(BaseHandler):
    POST_FIELDS = [
        POST_year, POST_credit, POST_term,
        POST_detail, POST_apply_remark,
        POST_user_id, POST_file_id,
        POST_project_id, POST_audit_department_id
    ]

    session_id = None

    def get(self):
        pass

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
            user = self.credit_user
            if user.id == params['user_id']:
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
            else:
                raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='用户身份有误, 请重新登录')
        except BaseException as e:
            db.session.rollback()
            raise e