#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 数据库配置

USER_NAME = 'manager_credit'
PASSWORD = 'TianTian1121@'
HOSTNAME = 'localhost'
DATABASE = 'creditdatabase'


class Config:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}/{}".format(USER_NAME, PASSWORD, HOSTNAME, DATABASE)

    LOG_PATH = os.path.join(basedir, 'logs/sc_credit_mis.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024
    LOG_FILE_BACKUP_COUNT = 10


class DevelopmentConfig(Config):
    pass


class TestingConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}



