#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
import datetime
import logging
import os
import random

from config import send_sms, qiniu
from config.db_mysql import Mysql
from config.db_redis import Redis
from config.secret import Secret
from config.send_email import SendEmail


class Config:
    # MySql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}?charset={}' \
        .format(Mysql.DATABASE_USER,
                Mysql.DATABASE_PWD, Mysql.HOSTNAME,
                Mysql.PORT, Mysql.DATABASE,
                Mysql.DATABASE_CHARSET)

    DEBUG = True
    # SQLALCHEMY配置
    # 记录打印SQL语句
    SQLALCHEMY_ECHO = True
    # 数据库连接池的大小
    SQLALCHEMY_POOL_SIZE = 5
    # 数据库连接池超时时间
    SQLALCHEMY_POOL_TIMEOUT = 9
    # 自动回收连接的秒数。这对MySQL是必须的，默认情况下MySQL会自动移除闲置8小时或者以上的连接,Flask-SQLAlchemy会自动地设置这个值为 2 小时。也就是说如果连接池中有连接2个小时被闲置，那么其会被断开和抛弃；
    SQLALCHEMY_POOL_RECYCLE = 9
    # 控制在连接池达到最大值后可以创建的连接数。当这些额外的连接使用后回收到连接池后将会被断开和抛弃。保证连接池只有设置的大小；
    SQLALCHEMY_MAX_OVERFLOW = 5
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存，如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = Secret.SECRET_KEY

    # 短信配置（网易云信）
    API_URL = send_sms.SendSms.API_URL
    APP_KEY = send_sms.SendSms.APP_KEY
    APP_SECRET = send_sms.SendSms.APP_SECRET
    NONCE = send_sms.SendSms.NONCE
    CODE_LEN = send_sms.SendSms.CODE_LEN
    TEMPLATE_ID = send_sms.SendSms.TEMPLATE_ID

    # 设置全局session失效时间
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=30)

    # 项目根路径
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    # 静态文件夹路径
    STATIC_DIR = os.path.join(BASE_DIR, 'static')
    # 模板文件夹路径
    TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
    # avatar头像上传路径
    UPLOADS_AVATAR = 'uploads/avatar/'
    UPLOADS_AVATAR_DIR = os.path.join(STATIC_DIR, UPLOADS_AVATAR)

    # 商品缩略图上传路径
    UPLOADS_GROUP_DEALS_THUMBNAIL_IMAGE = 'uploads/project/group_deals/thumbnail/'
    UPLOADS_GROUP_DEALS_THUMBNAIL_IMAGE_DIR = os.path.join(STATIC_DIR, UPLOADS_GROUP_DEALS_THUMBNAIL_IMAGE)

    UPLOADS_INNOVATION_THUMBNAIL_IMAGE = 'uploads/project/innovation/thumbnail/'
    UPLOADS_INNOVATION_THUMBNAIL_IMAGE_DIR = os.path.join(STATIC_DIR, UPLOADS_INNOVATION_THUMBNAIL_IMAGE)

    # 商品图上传路径
    UPLOADS_PROJECT_IMAGE = 'uploads/project/image/'
    UPLOADS_PROJECT_IMAGE_DIR = os.path.join(STATIC_DIR, UPLOADS_PROJECT_IMAGE)


    # 设置全局日志路径
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')

    # 初始化日志
    logger = logging.getLogger('leadNews_Flask')
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(LOGS_DIR + '/logs_info.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 允许上传图片的扩展名
    ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png']

    # 分页数据量
    PER_PAGE = 9

    # 七牛云配置
    QINIU_ACCESS_KEY = qiniu.QiNiu.QINIU_ACCESS_KEY
    QINIU_SECRET_KEY = qiniu.QiNiu.QINIU_SECRET_KEY
    QINIU_Q = qiniu.QiNiu.QINIU_Q
    QINIU_BUCKET_NAME = qiniu.QiNiu.QINIU_BUCKET_NAME
    QINIU_BUCKET = qiniu.QiNiu.QINIU_BUCKET
    CLOUD_IMG_URL = qiniu.QiNiu.CLOUD_IMG_URL

    # 缓存设置（Redis）
    REDIS_CONFIG = {
        'CACHE_TYPE': Redis.CACHE_TYPE,
        'CACHE_REDIS_HOST': Redis.CACHE_REDIS_HOST,
        'CACHE_REDIS_PORT': Redis.CACHE_REDIS_PORT
    }

    # 发送邮件
    MAIL_DEFAULT_SENDER = SendEmail.MAIL_DEFAULT_SENDER
    MAIL_SERVER = SendEmail.MAIL_SERVER
    MAIL_PORT = SendEmail.MAIL_PORT
    MAIL_USE_SSL = SendEmail.MAIL_USE_SSL
    MAIL_USE_TLS = SendEmail.MAIL_USE_TLS
    MAIL_USERNAME = SendEmail.MAIL_USERNAME
    MAIL_PASSWORD = SendEmail.MAIL_PASSWORD


class DevelopmentConfig(Config):
    ENV = 'deployment'
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_POOL_SIZE = 18
    SQLALCHEMY_POOL_TIMEOUT = 60
    SQLALCHEMY_POOL_RECYCLE = 18
    SQLALCHEMY_MAX_OVERFLOW = 9
    SQLALCHEMY_TRACK_MODIFICATIONS = False
