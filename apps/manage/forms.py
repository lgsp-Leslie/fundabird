#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
import uuid
from time import time

from flask import session
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, validators, PasswordField, SubmitField

from apps.models.manage_models import Admin
from config import constants
from config.exts import cache


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('Username', validators=[validators.DataRequired('Username field cannot be blank!')],
                           render_kw={
                               'class': 'ad-input',
                               'placeholder': 'Username',
                               'required': 'required'
                           })
    password = PasswordField('Password', validators=[validators.DataRequired('Password field cannot be blank!')],
                             render_kw={
                                 'class': 'ad-input',
                                 'placeholder': 'Password',
                                 'required': 'required'
                             })
    # verify_code = StringField('Verify Code', validators=[validators.DataRequired('Verify Code field cannot be blank!')],
    #                           render_kw={
    #                               'class': 'form-control',
    #                               'placeholder': 'Verify Code',
    #                               'required': 'required'
    #                           })
    submit = SubmitField(label='Login', render_kw={
        'class': 'ad-btn ad-login-member',
    })

    def validate(self):
        result = super().validate()
        username = self.username.data
        pwd = self.password.data
        # verify_code = self.verify_code.data
        if result:
            # if session.get('verify_code') and session.get('verify_code').lower() != verify_code.lower():
            #     result = False
            #     self.verify_code.errors = ['Your verify code is incorrect!']
            user_obj = Admin.query.filter_by(username=username).first()
            if user_obj is None:
                result = False
                self.password.errors = ['Your account or password is incorrect!']
            else:
                flag = check_password_hash(user_obj.password, pwd)
                if not flag:
                    result = False
                    self.password.errors = ['Your account or password is incorrect!']
                else:
                    if user_obj.user_status == constants.UserStatus.USER_IN_ACTIVE:
                        result = False
                        self.username.errors = ['Your account has been disabled!']
        return result

    def do_login(self):
        username = self.username.data
        user_obj = Admin.query.filter_by(username=username).first()
        session['uid'] = user_obj.id
        session['username'] = user_obj.username
        # 生成token
        token = uuid.uuid4().hex + str(round(time() * 1000))
        session['token'] = token
        # 创建集合
        cache_set_value = {token}
        # redis保存token
        cache.set(username, cache_set_value, timeout=5120)
        return user_obj
