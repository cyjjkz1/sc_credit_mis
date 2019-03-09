#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from handlers.user_handler import UserHandler, LoginHandler, LogoutHandler, ChangePasswordHandler
from handlers.upload_handler import UploadFileHandler

blue_print_user = Blueprint('blue_print_user', __name__, url_prefix='/credit/v1/api/user')
user_api = Api(blue_print_user)
user_api.add_resource(UserHandler, '/profile')
user_api.add_resource(LoginHandler, '/login')
user_api.add_resource(LogoutHandler, '/logout')
user_api.add_resource(ChangePasswordHandler, '/change_pwd')

blue_print_upload = Blueprint('blue_print_upload', __name__, url_prefix='/credit/v1/api/file')
upload_api = Api(blue_print_user)
upload_api.add_resource(UploadFileHandler, '/upload')

#user_api.add_resource('', '/logout')
#user_api.add_resource('', '/forget')
#
#
#blue_print_school = Blueprint('blue_print_school', __name__, url_prefix='/credit/v1/school')
#school_api = Api(blue_print_school)
#school_api.add_resource('', '/college/add')
#school_api.add_resource('', '/college/query')
#school_api.add_resource('', '/major/add')
#school_api.add_resource('', '/major/query')


