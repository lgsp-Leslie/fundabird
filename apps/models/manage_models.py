#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from datetime import datetime

from apps.models import BaseModel
from config import constants
from config.exts import db


class Admin(BaseModel):
    # 管理员表
    __tablename__ = 'manage_user'

    username = db.Column(db.String(50), unique=True, comment='用户名')
    password = db.Column(db.String(256), nullable=False, comment='密码')
    user_status = db.Column(db.Enum(constants.UserStatus), default=constants.UserStatus.USER_ACTIVE, comment='用户状态')
    user_role = db.Column(db.Enum(constants.UserRole), default=constants.UserRole.SUPER_ADMIN, comment='用户权限')
    avatar = db.Column(db.String(256), comment='头像')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='最后登录时间')

