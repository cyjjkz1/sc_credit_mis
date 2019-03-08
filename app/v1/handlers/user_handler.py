#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_restful import Resource
from ..models.user import Session, User
from flask import current_app as app
from flask import jsonify
from base_handler import with_credit_user, BaseHandler, HandlerException
from data_packer import RequiredField, converter
from data_packer.checker import (
    ReChecker
)
POST_accout = RequiredField('account', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,20}'))
POST_password = RequiredField('password', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9a-zA-Z]{8,20}'))


class UserHandler(BaseHandler):
    def get(self):
        app.logger.info('test get')
        self.gogo()
        return jsonify({'data': {}, 'respcd': '0000', 'respmsg': '请求成功'})

    @with_credit_user
    def gogo(self):
        pass


class LoginHandler(BaseHandler):
    POST_FIELDS = [
        POST_account, POST_password
    ]

    def post(self):
        ret = self.handle()
        if ret:
            return jsonify(ret)

    def _handle(self, *args, **kwargs):
        params = self.parse_request_params()
        app.logger.info('func=parse_request_params | parse_params = {} '.format(params))
        try:
            password = params['password']
            md5_pwd = self.md5(password)
            user = User.query.fiter_by(account=params['account'])
            if user.password == md5_pwd:
                # 密码正确，可以打cookie

                new_session_id = self.create_session_id()
                session = Session(session_id=new_session_id)
                session.save()
                return {'name': user.name}
            else:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))

        except BaseException as e:
            db.session.rollback()
            raise e

