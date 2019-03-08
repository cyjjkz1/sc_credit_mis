#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_restful import Resource
# from flask import request
from flask import current_app as app
from flask import jsonify
from base_handler import with_credit_user, BaseHandler
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

class LoginHandler(Resource):
    POST_FIELDS = [
        POST_account, POST_password
    ]
    def post(self):
        ret = self.handle()
        if ret:
            return jsonify(ret)

    def _handle(self, *args, **kwargs):
        pass

