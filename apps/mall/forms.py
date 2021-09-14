#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
import uuid
from time import time

from flask import session, g
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import validators, ValidationError, SubmitField, PasswordField
from wtforms.fields.html5 import EmailField

from apps.models.mall_models import User
from config import constants
from config.conf import Config
from config.exts import db, cache


class RegisterForm(FlaskForm):
    # 注册表单
    email = EmailField('Email', validators=[validators.DataRequired('Email field cannot be blank!')], render_kw={
        'class': 'form-control',
        'placeholder': 'Email',
        'required': 'required'
    })
    password = PasswordField('Password', validators=[validators.DataRequired('Password field cannot be blank!')],
                             render_kw={
                                 'class': 'form-control',
                                 'placeholder': 'Password',
                                 'required': 'required'
                             })
    re_password = PasswordField('Re-Password', validators=[validators.DataRequired('Re-Password field cannot be blank'),
                                                           validators.EqualTo('password',
                                                                              message='Entered passwords differ!')],
                                render_kw={
                                    'class': 'form-control',
                                    'placeholder': 'Re-Password',
                                    'required': 'required'
                                })
    submit = SubmitField(label='Sign Up', render_kw={
        'class': 'btn btn-block',
    })

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError('This email address already exists')
        return field

    def register(self):
        email = self.email.data
        pwd = self.password.data
        password = generate_password_hash(pwd)
        try:
            user_obj = User()
            user_obj.email = email
            user_obj.password = password
            db.session.add(user_obj)
            db.session.commit()
            return user_obj
        except Exception as e:
            Config.logger.info('注册失败—>%s' % e)
            return None


class LoginForm(FlaskForm):
    """登录表单"""
    email = EmailField('Email', validators=[validators.DataRequired('Email field cannot be blank!')], render_kw={
        'class': 'form-control',
        'placeholder': 'Email',
        'required': 'required'
    })
    password = PasswordField('Password', validators=[validators.DataRequired('Password field cannot be blank!')],
                             render_kw={
                                 'class': 'form-control',
                                 'placeholder': 'Password',
                                 'required': 'required'
                             })
    submit = SubmitField(label='Sign Up', render_kw={
        'class': 'btn btn-block',
    })

    def validate(self):
        result = super().validate()
        email = self.email.data
        pwd = self.password.data
        if result:
            user_obj = User.query.filter_by(email=email).first()
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
                        self.email.errors = ['Your account has been disabled!']
        return result

    def do_login(self):
        email = self.email.data
        user_obj = User.query.filter_by(email=email).first()
        session['uid'] = user_obj.id
        session['email'] = user_obj.email
        # 生成token
        token = uuid.uuid4().hex + str(round(time() * 1000))
        session['token'] = token
        # 创建集合
        cache_set_value = {token}
        # redis保存token
        cache.set(str(user_obj.id), cache_set_value, timeout=5120)
        return user_obj
