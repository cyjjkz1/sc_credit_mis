#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_restful import Resource
# from flask import request
from flask import current_app as app
from flask import jsonify
from base_handler import with_credit_user


class UserHandler(Resource):

    @with_credit_user
    def get(self):
        app.logger.info('test get')
        return jsonify({'data': {}, 'respcd': '0000', 'respmsg': '请求成功'})


class LoginHandler(Resource):
    def post(self):
        pass

