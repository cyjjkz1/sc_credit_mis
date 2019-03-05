#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from handlers.user_handler import UserHandler


blue_print_user = Blueprint('blue_print_user', __name__, url_prefix='/credit/v1/user')
user_api = Api(blue_print_user)
user_api.add_resource(UserHandler, '/profile')
user_api.add_resource('', '/login')
user_api.add_resource('', '/logout')
user_api.add_resource('', '/forget')


blue_print_school = Blueprint('blue_print_school', __name__, url_prefix='/credit/v1/school')
school_api = Api(blue_print_school)
school_api.add_resource('', '/college/add')
school_api.add_resource('', '/college/query')
school_api.add_resource('', '/major/add')
school_api.add_resource('', '/major/query')


