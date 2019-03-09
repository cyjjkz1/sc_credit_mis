#!/usr/bin/env python
# -*- coding:utf-8 -*-
#from flask_restful import Resource
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
POST_account = RequiredField('account', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9]{1,20}'))
POST_password = RequiredField('password', converter=converter.TypeConverter(str), checker=ReChecker(r'[0-9a-zA-Z]{6,20}'))


class UserHandler(BaseHandler):
    def get(self):
        ret = self.handle()
        return jsonify(ret)

    @with_credit_user
    def _handle(self, *args, **kwargs):
        try:
            user = self.credit_user
            if user is None:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))
            return user.to_json()
        except BaseException as e:
            db.session.rollback()
            raise e


class LoginHandler(BaseHandler):
    POST_FIELDS = [
        POST_account, POST_password
    ]

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
            app.logger.info('user query | user info = {}'.format(user.to_json()))

            if user.password == md5_pwd:
                # 密码正确，可以打cookie
                if user.session:
                    db.session.delte(user.session)
                    db.session.commit()
                new_session_id = self.create_session_id()
                self.session_id = new_session_id
                session = Session(session_id=new_session_id)
                session.user = user
                session.save()
                return user.to_json()
            else:
                raise HandlerException(respcd=RESP_CODE.DB_ERROR, respmsg=RESP_ERR_MSG.get(RESP_CODE.DB_ERROR))

        except BaseException as e:
            db.session.rollback()
            raise e


class LogoutHandler(BaseHandler):
    def post(self):
        ret = self.handle()
        return jsonify(ret)

    def _handle(self, *args, **kwargs):
        try:
            user = self.credit_user
            app.logger.info("account = {} 退出登陆".format(user.account))
            session = user.session
            db.session.delete(session)
            db.session.commit()
            return {}
        except BaseException as e:
            db.session.rollback()
            raise e

