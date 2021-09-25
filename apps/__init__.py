#!/usr/bin/env python3
# coding=utf-8
# File:__init__.py.py
# Author:LGSP_Harold
from flask import Flask

from apps.manage.views import manage_bp
from config import conf
from config.exts import cors, cache, migrate, mail

from apps.models import *

from apps.utils.views import utils_bp


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # 生产环境需修改成ProductionConfig
    app.config.from_object(conf.DevelopmentConfig)

    # 初始化SQLAlchemy
    db.init_app(app=app)
    # 初始化flask-migrate
    migrate.init_app(app, db)
    # 初始化跨域
    cors.init_app(app=app, supports_credentials=True)
    # 初始化缓存文件
    cache.init_app(app=app, config=conf.Config.REDIS_CONFIG)
    # 初始化发送邮件
    mail.init_app(app)

    # 注册蓝图
    app.register_blueprint(utils_bp, url_prefix='/utils')
    app.register_blueprint(manage_bp, url_prefix='/manage')

    return app
