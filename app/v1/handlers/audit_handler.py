#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from flask_restful import Resource
from ..models.apply_record import ApplyRecord
from flask import current_app as app
from flask import jsonify, make_response, request
from base_handler import with_credit_user, BaseHandler, HandlerException
from data_packer import RequiredField, converter
from data_packer.checker import (
    ReChecker, LenChecker
)
from app import db
from ..constant import RESP_CODE

POST_record_id = RequiredField('record_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,}'))
POST_audit_credit = RequiredField('audit_credit', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1}'))
POST_audit_remark = RequiredField('audit_remark',
                                  converter=converter.TypeConverter(str),
                                  checker=LenChecker(max_len=200, min_len=0))


class AuditHandler(BaseHandler):
    POST_FIELDS = [
        POST_record_id, POST_audit_credit, POST_audit_remark
    ]
    session_id = None

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
                if userid:
                    apply_record_id = params['record_id']
                    audit_credit = params['audit_credit']
                    audit_remark = params['audit_remark']
                    record = ApplyRecord.query.filter(ApplyRecord.id == apply_record_id).first()
                    record.audit_credit = audit_credit
                    record.audit_remark = audit_remark
                    record.save()
                    return {'recod_id': str(record.id), 'audit_credit': audit_remark}
                else:
                    raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='用户身份有误, 请重新登录')
        except BaseException as e:
            db.session.rollback()
            raise e
