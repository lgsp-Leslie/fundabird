#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from flask import Blueprint, session, redirect, url_for, g, request, flash, render_template

from apps.manage.forms import LoginForm
from apps.models.mall_models import User
from apps.models.manage_models import Admin
from config.conf import Config

manage_bp = Blueprint('manage', __name__)


@manage_bp.route('/logout')
def logout():
    session.clear()
    g.user = None
    return redirect(url_for('manage.login'))


@manage_bp.route('/login', methods=['GET', 'POST'])
def login():
    token = session.get('token')
    if token:
        return redirect(url_for('manage.index'))

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_obj = form.do_login()
            if user_obj:
                flash('Welcome to login!', 'success')
                return redirect(url_for('manage.index'))
    return render_template('background/accounts/login.html', form=form)


@manage_bp.route('/index')
def index():
    return render_template('background/accounts/index.html')


@manage_bp.route('/user_list')
def user_list():
    page = int(request.args.get('page', 1))
    page_data = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('background/accounts/user_list.html', page_data=page_data)


@manage_bp.route('/user_detail')
def user_detail():
    uid = request.args.get('uid')
    user = User.query.get(uid)
    if user is None:
        flash('User does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.user_list'))
    return render_template('background/accounts/user_detail.html', user=user)


@manage_bp.route('/admin_list')
def admin_list():
    page = int(request.args.get('page', 1))
    page_data = Admin.query.order_by(Admin.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('background/accounts/admin_list.html', page_data=page_data)
