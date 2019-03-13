#!/usr/bin/env python
# -*- coding:utf-8 -*-
# from flask_restful import Resource
from ..models.user import Session, User
from flask import current_app as app
from flask import jsonify, make_response
from base_handler import with_credit_user, BaseHandler, HandlerException
from data_packer import RequiredField, converter
from data_packer.checker import (
    ReChecker
)
from app import db
from ..constant import RESP_CODE, RESP_ERR_MSG
POST_year = RequiredField('year', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9~]{1,20}'))
POST_credit = RequiredField('credit', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1}'))
POST_term = RequiredField('term', converter=converter.TypeConverter(str), checker=ReChecker(r'[12]{1}'))
POST_detail = RequiredField('detail', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,20}'))
POST_apply_remark = RequiredField('apply_remark',
                                  converter=converter.TypeConverter(str),
                                  checker=ReChecker(r'[0-9a-zA-Z]{6,20}'))
POST_user_id = RequiredField('userid', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9~]{1,}'))
POST_file_id = RequiredField('file_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9~]{1,}'))
POST_project_id = RequiredField('project_id', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9~]{1,}'))


class ApplyHandler(BaseHandler):
    def get(self):
        pass

    def post(self):
        POST_FIELDS = [
            POST_account, POST_password, POST_role
        ]
        session_id = None

        def post(self):
            ret = self.handle()
            resp = make_response(jsonify(ret), 200)
            if self.session_id:
                app.logger.info('sessionid={}'.format(self.session_id))
                resp.set_cookie('sessionid', self.session_id)
            return resp

        def _handle(self, *args, **kwargs):
            params = self.parse_request_params()
            app.logger.info('func=parse_request_params | parse_params = {} '.format(params))
            try:
                password = params['password']
                md5_pwd = self.md5(password)
                user = User.query.filter_by(account=params['account']).first()
                app.logger.info('user query | user info = {}'.format(user.to_dict()))

                if user.password == md5_pwd:
                    if str(user.role) != str(params['role']):
                        raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='用户角色错误')

                    # 密码正确，可以打cookie
                    if user.session.first() is not None:
                        db.session.delete(user.session.first())
                        db.session.commit()
                    new_session_id = self.create_session_id()
                    self.session_id = new_session_id
                    session = Session(session_id=new_session_id)
                    session.user = user
                    session.save()
                    return {'sessionid': new_session_id}
                else:
                    raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='密码错误，请重新输入密码')

            except BaseException as e:
                db.session.rollback()
                raise e