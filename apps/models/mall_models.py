#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from datetime import datetime

from apps.models import BaseModel
from config import constants
from config.exts import db


class User(BaseModel):
    # 用户表
    __tablename__ = 'mall_user'

    email = db.Column(db.String(50), nullable=False, unique=True, comment='邮箱')
    password = db.Column(db.String(256), nullable=False, comment='密码')
    donations = db.Column(db.Integer, default=0, comment='捐赠总额')
    coins = db.Column(db.Integer, default=0, comment='虚拟币$1=1')
    user_status = db.Column(db.Enum(constants.UserStatus), default=constants.UserStatus.USER_ACTIVE, comment='用户状态')
    email_status = db.Column(db.Enum(constants.EmailStatus), default=constants.EmailStatus.EMAIL_IN_ACTIVE,
                             comment='邮箱状态')
    user_role = db.Column(db.Enum(constants.UserRole), default=constants.UserRole.COMMON, comment='用户权限')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='最后登录时间')


class ShippingAddress(BaseModel):
    # 邮寄地址表
    __tablename__ = 'mall_user_shipping_addr'

    first_name = db.Column(db.String(50), nullable=False, comment='名字')
    last_name = db.Column(db.String(50), nullable=False, comment='姓氏')
    address1 = db.Column(db.String(256), nullable=False, comment='收货地址1')
    address2 = db.Column(db.String(256), comment='收货地址2')
    zipcode = db.Column(db.String(20), comment='状态/邮编')
    country = db.Column(db.String(30), comment='国家')

    user_id = db.Column(db.Integer, db.ForeignKey('mall_user.id'))
    user = db.relationship('User', backref='shipping_address')


class BankCardInfo(BaseModel):
    # 银行卡信息表
    __tablename__ = 'mall_user_bank_card'

    card_number = db.Column(db.String(50), nullable=False, comment='银行卡号')
    card_name = db.Column(db.String(30), comment='银行卡名称')
    card_exp = db.Column(db.String(5), nullable=False, comment='银行卡有效期')
    card_cw = db.Column(db.String(3), nullable=False, comment='银行卡安全码')

    user_id = db.Column(db.Integer, db.ForeignKey('mall_user.id'))
    user = db.relationship('User', backref='bank_card_info')


