#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ..models.apply_record import ApplyFile
from flask import current_app as app
from flask import request, jsonify
from base_handler import with_credit_user, BaseHandler, HandlerException
from app import db
from ..constant import RESP_CODE, files_base_url
import os
import datetime
ALLOWED_EXTENSIONS = set([
    'doc', 'docx',
    'xls', 'xlsx',
    'png', 'jpg',
    'JPG', 'PNG',
    'gif', 'GIF',
    'pdf'
])


class UploadFileHandler(BaseHandler):
    def post(self):
        ret = self.handle()
        return jsonify({ret})

    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

    @with_credit_user
    def _handle(self, *args, **kwargs):
        if 'file' not in request.files:
            app.logger.info('No file part')
            raise HandlerException(respcd=RESP_CODE.PARAM_ERROR, respmsg='没有获取到上传文件')
        file = request.files['file']

        if file.filename == '':
            app.logger.info('No selected file')
            raise HandlerException(respcd=RESP_CODE.PARAM_ERROR, respmsg='没有获取到上传文件')
        else:
            try:
                if file and self.allowed_file(file.filename):
                    origin_file_name = file.filename
                    app.logger.info('filename is %s' % origin_file_name)
                    # filename = secure_filename(file.filename)
                    ext = origin_file_name.rsplit('.', 1)[1]
                    now_time = datetime.datetime.now()
                    filename = now_time.strftime('%Y%m%d%H%M%S%f') + '.' + ext
                    if os.path.exists(files_base_url):
                        app.logger.debug('%s path exist' % files_base_url)
                        pass
                    else:
                        app.logger.debug('%s path not exist, do make dir' % files_base_url)
                        os.makedirs(files_base_url)

                    file.save(os.path.join(files_base_url, filename))
                    apply_file = ApplyFile(filename)
                    apply_file.save()
                    app.logger.debug('%s save successfully' % filename)
                    return {'filename': filename}
                else:
                    app.logger.debug('%s not allowed' % file.filename)
                    raise HandlerException(respcd=RESP_CODE.PARAM_ERROR, respmsg='上传文件格式错误')
            except BaseException as e:
                db.session.rollback()
                app.logger.debug('upload file exception: %s' % e)
                raise e

