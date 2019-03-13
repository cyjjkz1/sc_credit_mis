#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    # 应用配置
    app.config.from_object(config[config_name])
    app.config['JSON_AS_ASCII'] = False

    # 配置数据库
    db.init_app(app)

    # 配置蓝图
    from v1.urls import blue_print_user, blue_print_upload, blue_print_project
    app.register_blueprint(blue_print_user)
    app.register_blueprint(blue_print_upload)
    app.register_blueprint(blue_print_project)
    # 配置日志
    import logging
    from logging.handlers import RotatingFileHandler
    # Formatter
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(process)d %(thread)d %(pathname)s %(lineno)s %(message)s")
    # FileHandler Info
    file_handler_info = RotatingFileHandler(filename=config[config_name].LOG_PATH)
    file_handler_info.setFormatter(formatter)
    app.logger.addHandler(file_handler_info)
    app.logger.setLevel(logging.INFO)

    return app


if __name__ == '__main__':
    scApp = create_app()
    scApp.run(host='0.0.0.0', port=9090)

