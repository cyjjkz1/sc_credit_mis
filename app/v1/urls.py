#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask_restful import Api
from handlers.user_handler import UserHandler, LoginHandler, LogoutHandler, ChangePasswordHandler
from handlers.upload_handler import UploadFileHandler, DownloadHandle
from handlers.project_handler import ProjectHandler
from handlers.apply_handler import ApplyHandler, RecordListHandler, DepartmentStatusRecordsHandler, DepartmentAllRecordsHandler
from handlers.audit_handler import AuditHandler
blue_print_user = Blueprint('blue_print_user', __name__, url_prefix='/credit/v1/api/user')
user_api = Api(blue_print_user)
user_api.add_resource(UserHandler, '/profile')
user_api.add_resource(LoginHandler, '/login')
user_api.add_resource(LogoutHandler, '/logout')
user_api.add_resource(ChangePasswordHandler, '/change_pwd')

blue_print_upload = Blueprint('blue_print_upload', __name__, url_prefix='/credit/v1/api/file')
upload_api = Api(blue_print_upload)
upload_api.add_resource(UploadFileHandler, '/upload')
upload_api.add_resource(DownloadHandle, '/download/<filename>')

blue_print_project = Blueprint('blue_print_project', __name__, url_prefix='/credit/v1/api/project')
project_api = Api(blue_print_project)
project_api.add_resource(ProjectHandler, '/query')

blue_print_apply = Blueprint('blue_print_apply', __name__, url_prefix='/credit/v1/api/apply')
apply_api = Api(blue_print_apply)
apply_api.add_resource(ApplyHandler, '/submit', endpoint='aupply_submit')
apply_api.add_resource(ApplyHandler, '/info', endpoint='aupply_info')
apply_api.add_resource(RecordListHandler, '/list')

apply_api.add_resource(DepartmentStatusRecordsHandler, '/department/list')
apply_api.add_resource(DepartmentAllRecordsHandler, '/department/wait_audit')
apply_api.add_resource(AuditHandler, '/audit', endpoint='aupply_audit')


#user_api.add_resource('', '/forget')
#
#
#blue_print_school = Blueprint('blue_print_school', __name__, url_prefix='/credit/v1/school')
#school_api = Api(blue_print_school)
#school_api.add_resource('', '/college/add')
#school_api.add_resource('', '/college/query')
#school_api.add_resource('', '/major/add')
#school_api.add_resource('', '/major/query')


