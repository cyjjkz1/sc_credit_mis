#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ..models.user import Session, User
from flask import current_app as app
from flask import jsonify
from base_handler import with_credit_user, BaseHandler, HandlerException
from app import db
from ..constant import RESP_CODE, RESP_ERR_MSG, files_base_url


class UploadFileHandler(BaseHandler):
    def post(self):
        return jsonify({'path': files_base_url})

    def _handle(self, *args, **kwargs):


        # params = self.parse_request_params()
        # app.logger.info('func=parse_request_params | parse_params = {} '.format(params))
        try:
            pass
        #     password = params['password']
        #     md5_pwd = self.md5(password)
        #     user = User.query.filter_by(account=params['account']).first()
        #     app.logger.info('user query | user info = {}'.format(user.to_json()))
        #
        #     if user.password == md5_pwd:
        #         if user.role != params['role']:
        #             raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='用户角色错误')
        #
        #         # 密码正确，可以打cookie
        #         if user.session.first() is not None:
        #             db.session.delete(user.session.first())
        #             db.session.commit()
        #         new_session_id = self.create_session_id()
        #         self.session_id = new_session_id
        #         session = Session(session_id=new_session_id)
        #         session.user = user
        #         session.save()
        #         return {'sessionid': new_session_id}
        #     else:
        #         raise HandlerException(respcd=RESP_CODE.USER_NOT_LOGIN, respmsg='密码错误，请重新输入密码')

        except BaseException as e:
            db.session.rollback()
            raise e