#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from config import constants
from config.exts import db


class SeoConf(db.Model):
    __tablename__ = 'config_seo_conf'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), comment='首页Title')
    keywords = db.Column(db.String(256), comment='关键字')
    description = db.Column(db.String(512), comment='描述信息')


class FindUs(db.Model):
    __tablename__ = 'config_find_us_conf'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(30), comment='联系电话')
    email = db.Column(db.String(50), comment='联系邮箱')
    address = db.Column(db.String(256), comment='联系地址')
    facebook = db.Column(db.String(1024), comment='facebook')
    instagram = db.Column(db.String(1024), comment='instagram')
    twitter = db.Column(db.String(1024), comment='twitter')
    wechat = db.Column(db.String(1024), comment='wechat')


class SendEmail(db.Model):
    # 发送邮件配置表
    __tablename__ = 'config_send_email'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(128), nullable=False, comment='发送主题')
    sender = db.Column(db.String(128), nullable=False, comment='发件人')
    server = db.Column(db.String(50), nullable=False, comment='Email服务器地址')
    port = db.Column(db.SmallInteger, nullable=False, comment='端口')
    use_ssl = db.Column(db.Boolean, default=True, comment='SSL加密通信')
    username = db.Column(db.String(50), nullable=False, comment='邮箱账号')
    password = db.Column(db.String(256), nullable=False, comment='邮箱密码/授权码')
    use_type = db.Column(db.Enum(constants.SendEmailType), default=constants.SendEmailType.NONE, comment='用途')


class NationalCity(db.Model):
    # 国家城市表
    __tablename__ = 'config_national_city'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    national = db.Column(db.String(20), nullable=False, comment='国家')
    state_full = db.Column(db.String(20), comment='州')
    state_short = db.Column(db.String(20), nullable=False, comment='州(简称)')
    county = db.Column(db.String(20), nullable=False, comment='县')
    city = db.Column(db.String(20), nullable=False, comment='城市')
