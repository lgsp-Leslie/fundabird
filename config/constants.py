#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
""" 常量配置 """
from enum import Enum


class UserStatus(Enum):
    """ 用户状态 """
    # 启用，可以登录系统
    USER_ACTIVE = 'Enable'
    # 禁用，不能登录系统
    USER_IN_ACTIVE = 'Disable'


class EmailStatus(Enum):
    """ 邮箱验证状态 """
    # 验证
    EMAIL_ACTIVE = 'Verified'
    # 未认证
    EMAIL_IN_ACTIVE = 'Not Verified'


class UserRole(Enum):
    """ 用户角色 """
    # 普通用户
    COMMON = 'COMMON'
    # 管理员
    ADMIN = 'ADMIN'
    # 超级管理员
    SUPER_ADMIN = 'SUPER_ADMIN'


class SendEmailType(Enum):
    """ 发送邮件类型 """
    # 禁用
    NONE = 'None'
    # 注册
    REGISTER = 'Register'
    # 重置密码
    RESET_PASSWORD = 'Reset Password'


class ProductStatus(Enum):
    """ 商品状态 """
    # 预热
    PREHEAT = 'Preheat'
    # 众筹中
    CROWD_FUNDING = 'Crowd Funding'

    # 待审核
    PENDING = 'Pending'
    # 审核通过
    APPROVED = 'Approved'
    # 审核不通过（不可修改）
    REJECTED = 'Rejected'
    # 审核不通过（可修改）
    RESUBMIT = 'Resubmit'
    # 项目结束
    FINISH = 'Finish'


class OnlineStatus(Enum):
    # 用户在线状态
    ONLINE = 'Online'
    NOT_ONLINE = 'Not Online'
