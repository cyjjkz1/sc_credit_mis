#!/usr/bin/env python
# -*- coding:utf-8 -*-
import traceback
import json
from data_packer import DataPacker
from data_packer.err import DataPackerError, DataPackerCheckError, DataPackerSrcKeyNotFoundError
from data_packer.container import DictContainer
from flask import current_app as app
from flask_restful import Resource
from flask import request, abort
from app.v1.constant import RESP_CODE, RESP_ERR_MSG
from pymysql import err
import functools
from ..models.user import Session
import datetime
import hashlib
import random
import string


def with_credit_user(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        app.logger.info("cookie=%s", request.cookies)
        sessionid = request.cookies.get('sessionid')
        if sessionid is None:
            app.logger.info('未登陆')
            return self.request_finish(RESP_CODE.USER_NOT_LOGIN, resperr=RESP_ERR_MSG.get(RESP_CODE.USER_NOT_LOGIN))

        se = Session.query.filter_by(session_id=self.sessionid).first()
        if se:
            self.credit_user = se.user

            exp = se.expire
            create_time = se.create_time
            now = datetime.datetime.now()
            exp_time = create_time + datetime.timedelta(days=exp)
            diff = exp_time - now
            diff_seconds = diff.days * 86400 + diff.seconds
            if diff_seconds > 0:
                app.logger.info('未登陆')
                return self.request_finish(RESP_CODE.USER_NOT_LOGIN, resperr=RESP_ERR_MSG.get(RESP_CODE.USER_NOT_LOGIN))
            app.logger.info('sessionid: %s, userid: %s', self.sessionid, self.credit_user.id)
        else:
            app.logger.info('未登陆')
            return self.request_finish(RESP_CODE.USER_NOT_LOGIN, resperr=RESP_ERR_MSG.get(RESP_CODE.USER_NOT_LOGIN))
        return func(self, *args, **kwargs)
    return wrapper


class HandlerException(Exception):
    def __init__(self, respcd, respmsg=''):
        self.respcd = respcd
        self.respmsg = respmsg


class BaseHandler(Resource):
    GET_FIELDS = []
    POST_FIELDS = []

    def handle(self, *args, **kwargs):
        try:
            app.logger.info('<<<< Start %s.%s>>>>', self.__class__.__module__, self.__class__.__name__)
            ret = self._handle(*args, **kwargs)
            if ret:
                app.logger.info('func=_handle|_handle_ret_params=%s', ret)
                ret = self.request_finish(respcd=RESP_CODE.SUCCESS,
                                          respmsg='',
                                          resperr=RESP_ERR_MSG.get(RESP_CODE.SUCCESS),
                                          data=ret)
                app.logger.info('func=request_finish|request_finish_params=%s', ret)
                app.logger.info('<<<< END %s.%s >>>>', self.__class__.__module__, self.__class__.__name__)
                return ret
            else:
                app.logger.info('func=handle| 没有返回处理结果')
        except HandlerException as e:
            app.logger.warn(traceback.format_exc())
            return self.request_finish(e.respcd, resperr=e.respmsg)
        except BaseException as e:
            app.logger.warn(traceback.format_exc())
            app.logger.warn(e.message)
            return abort(500)

    def _handle(self, *args, **kwargs):
        raise NotImplementedError()

    def parse_request_params(self, check_param=True):
        """
        解析客户端请求的数据，并返回dict
        :param check_param: 是否检查参数
        :param error_message:
        :return:
        """
        app.logger.info(request.headers)
        app.logger.info(request.form)
        app.logger.info(request.values)
        app.logger.info(request.args)
        app.logger.info(request.data)
        try:
            if request.method == 'GET':
                req_params = request.args
            elif request.method == 'POST':
                req_params = json.loads(request.data)
            else:
                raise HandlerException(RESP_CODE.MEHTOD_NOT_FOUND, error_message=request.method)

            if check_param:
                checked_req_param = self.check_params(req_params)
                app.logger.info('func=check_params|checked_req_param=%s', checked_req_param)
                return checked_req_param
        except HandlerException as e:
            app.logger.warn(traceback.format_exc())
            app.logger.warn(e.message)
            raise e
        except BaseException as e:
            app.logger.warn(traceback.format_exc())
            app.logger.warn(e.message)
            return abort(500)

    def check_params(self, params):
        ret = {}
        check_fileds = []
        if request.method == 'GET':
            check_fileds = self.GET_FIELDS
        elif request.method == 'POST':
            check_fileds = self.POST_FIELDS
        else:
            pass

        dp = DataPacker(check_fileds)
        try:
            dp.run(
                DictContainer(params),
                DictContainer(ret)
            )
            return ret
        except DataPackerCheckError as e:
            app.logger.warn(traceback.format_exc())
            app.logger.warn('{} 校验错误 {}'.format(e.src_name, type(e), str(e)))
            err_msg = RESP_ERR_MSG.get(RESP_CODE.PARAM_ERROR, '') + ' : {} 校验错误'.format(e.src_name)
            raise HandlerException(RESP_CODE.PARAM_ERROR, resperr=err_msg)

        except DataPackerSrcKeyNotFoundError as e:
            app.logger.warn(traceback.format_exc())
            app.logger.warn('{} 校验错误 {}'.format(e.src_name, type(e), str(e)))
            err_msg = RESP_ERR_MSG.get(RESP_CODE.PARAM_ERROR, '') + ' 缺少参数: {}'.format(e.src_name)
            raise HandlerException(RESP_CODE.PARAM_ERROR, resperr=err_msg)
        except DataPackerError as e:
            app.logger.warn(traceback.format_exc())
            app.logger.warn('{} 校验错误 {}'.format(e.src_name, type(e), str(e)))
            err_msg = RESP_ERR_MSG.get(RESP_CODE.PARAM_ERROR, '') + ' : {} 字段错误'.format(e.src_name)
            raise HandlerException(RESP_CODE.PARAM_ERROR, resperr=err_msg)

        finally:
            pass

    def request_finish(self, respcd, respmsg='', resperr='', **kwargs):
        if not resperr:
            resperr = RESP_ERR_MSG.get(respcd, '')
        resp = {
            'respcd': respcd,
            'respmsg': respmsg,
            'resperr': resperr
        }
        resp.update(kwargs)
        return resp

    def md5(self, text):
        m = hashlib.md5()
        m.update(text.encode('UTF-8'))
        return m.hexdigest()

    def create_session_id(self):
        return self.md5(''.join(random.sample(string.ascii_letters + string.digits, 20)))
