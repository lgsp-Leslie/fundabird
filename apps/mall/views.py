#!/usr/bin/env python3
# coding=utf-8
# Version:python3.6.1
# Project:flaskLeadNewsProject
# File:views.py
# Data:2021/8/24 10:46
# Author:LGSP_Harold
from flask import Blueprint, render_template, flash, redirect, url_for, request, session, g

from apps.mall.forms import RegisterForm, LoginForm
from apps.models.config_models import SendEmail
from apps.utils.utils import send_email

mall_bp = Blueprint('mall', __name__)


@mall_bp.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('mall.index'))


@mall_bp.route('/login', methods=['GET', 'POST'])
def login():
    token = session.get('token')
    if token:
        return redirect(url_for('mall.index'))

    form = LoginForm()
    next_url = request.values.get('next', url_for('mall.index'))
    if request.method == 'POST':
        if form.validate_on_submit():
            user_obj = form.do_login()
            if user_obj:
                flash('Welcome to login!', 'success')
                return redirect(next_url)
    return render_template('foreground/accounts/login.html', form=form)


@mall_bp.route('/register', methods=['GET', 'POST'])
def register():
    token = session.get('token')
    if token:
        return redirect(url_for('mall.index'))

    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_obj = form.register()
            if user_obj:
                flash('Registration succeeded, please login!', 'success')
                send_email_obj = SendEmail.query.filter_by(use_type='REGISTER').first()
                send_email(user_obj.id, send_email_obj.sender, send_email_obj.subject, user_obj.email, '/foreground/accounts/verification_email.html')

                return redirect(url_for('mall.login'))
            else:
                flash('Registration failed, please try again later!', 'danger')
    return render_template('foreground/accounts/register.html', form=form)


@mall_bp.route('/index')
@mall_bp.route('/')
def index():
    return render_template('foreground/index.html')
