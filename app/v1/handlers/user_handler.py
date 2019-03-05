#!/usr/bin/env python
# -*- coding:utf-8 -*-
from flask_restful import Resource
#from flask import request
from flask import current_app as app
from flask import jsonify
class UserHandler(Resource):
    def get(self):
        app.logger.info('test get')
        return jsonify({'aa': 'bb'})
