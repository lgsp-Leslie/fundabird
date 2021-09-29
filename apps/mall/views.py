#!/usr/bin/env python3
# coding=utf-8
# Version:python3.6.1
# Project:flaskLeadNewsProject
# File:views.py
# Data:2021/8/24 10:46
# Author:LGSP_Harold
import uuid
from time import time

import requests
from flask import Blueprint, render_template, flash, redirect, url_for, request, session, g, jsonify
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from apps.mall.forms import RegisterForm, LoginForm
from apps.models.config_models import SendEmail
from apps.models.mall_models import User, BankCardInfo, Product
from apps.utils.utils import send_email, upload_file
from config import constants
from config.conf import Config
from config.exts import db, cache

mall_bp = Blueprint('mall', __name__)


@mall_bp.route('/logout')
def logout():
    # 登出
    session.clear()
    g.user = None
    return redirect(url_for('mall.index'))


@mall_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 登录
    uid = session.get('uid')
    token = session.get('token')
    if uid and token:
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


@mall_bp.route('/fb_login', methods=['POST'])
def fb_login():
    token = session.get('token')
    if token:
        return redirect(url_for('mall.index'))
    next_url = request.values.get('next', url_for('mall.index'))
    fb_status = request.form.get('fb_status')
    if fb_status == 'not_authorized':
        flash('您必须授权才能登录！')
        return redirect(url_for('mall.login'))
    elif fb_status == 'connected':
        fb_email = request.form.get('fb_email')
        # 验证第三方token是否正确
        fb_token = request.form.get('fb_token')
        fb_check_url = 'https://graph.facebook.com/debug_token?access_token=2915084535468883%7Ca56e2a174b69202ebfa04aa62663fb34&input_token=' + fb_token
        response = requests.get(url=fb_check_url)
        data = response.json().get('data')

        if fb_email and data['is_valid']:
            user_obj = User.query.filter_by(bind_facebook=fb_email).first()
            if user_obj is None:
                email = fb_email
                try:
                    user_obj = User()
                    user_obj.email = email
                    user_obj.bind_facebook = email
                    user_obj.user_login_type = 'Facebook'
                    db.session.add(user_obj)
                    db.session.commit()
                except Exception as e:
                    Config.logger.info('注册失败—>%s' % e)
                    flash('服务器繁忙，请稍后再试！')
                    print(e)
                    return redirect(url_for('mall.index'))
            user_obj = User.query.filter_by(bind_facebook=fb_email).first()
            session['uid'] = user_obj.id
            session['email'] = user_obj.email
            # 生成token
            token = uuid.uuid4().hex + str(round(time() * 1000))
            session['token'] = token
            # 创建集合
            cache_set_value = {token}
            # redis保存token
            cache.set(str(user_obj.id), cache_set_value, timeout=5120)
            send_email_obj = SendEmail.query.filter_by(use_type='REGISTER').first()
            send_email(subject='邮箱地址验证', addressee=user_obj.email, template='foreground/email/verification_email.html', user_id=user_obj.id)
            flash('Welcome to login!', 'success')
            return jsonify({'code': 200, 'msg': '登录成功'})
        else:
            flash('您必须授权您的邮箱账号')
            return jsonify({'code': 400, 'msg': '登录失败'})


@mall_bp.route('/register', methods=['GET', 'POST'])
def register():
    # 注册
    token = session.get('token')
    if token:
        return redirect(url_for('mall.index'))

    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_obj = form.register()
            if user_obj:
                flash('Registration succeeded, please login!', 'success')
                # send_email_obj = SendEmail.query.filter_by(use_type='REGISTER').first()
                send_email(subject='邮箱地址验证', addressee=user_obj.email, template='foreground/email/verification_email.html', user_id=user_obj.id)
                return redirect(url_for('mall.login'))
            else:
                flash('Registration failed, please try again later!', 'danger')
    return render_template('foreground/accounts/register.html', form=form)


@mall_bp.route('/check_email')
def check_email():
    # 重新发送验证邮件
    send_email(subject='邮箱地址验证', addressee=g.user.email, template='foreground/email/verification_email.html', user_id=g.user.id)
    return redirect(url_for('mall.index'))


@mall_bp.route('/modify_email')
def modify_email():
    # 修改email
    email = request.args.get('email', None)
    if email is None:
        return jsonify(code=400, msg='Modification failed,  email address cannot be empty!')
    user_obj = User.query.filter(User.email == email).first()
    if user_obj:
        return jsonify(code=400, msg='Modification failed, the email address has been registered!')
    else:
        user = User.query.get(g.user.id)
        user.email = email
        user.email_status = constants.EmailStatus.EMAIL_IN_ACTIVE
        db.session.commit()
        user_obj = User.query.filter(User.email == email).first()
        send_email(subject='邮箱地址验证', addressee=user_obj.email, template='foreground/email/verification_email.html', user_id=user_obj.id)
        return jsonify(code=200, msg='Modification succeeded. Verification email has been sent to this email address!')


@mall_bp.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    card = BankCardInfo.query.filter_by(user_id=g.user.id).all()

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        user = User.query.get(g.user.id)

        avatar = request.files.get('avatar')
        if avatar:
            avatar_name = upload_file(avatar, Config.UPLOADS_AVATAR_DIR)
            if avatar_name is not None:
                file_path = Config.UPLOADS_AVATAR_DIR + avatar_name
                avatar.save(file_path)
                user.avatar = Config.UPLOADS_AVATAR + avatar_name
            else:
                flash('User avatar image format is not supported!', 'danger')
        old_email = user.email
        if email != old_email:
            user_email = User.query.filter_by(email=email).first()
            if user_email:
                flash('Email address already exists!', 'danger')
                return render_template('foreground/accounts/edit_profile.html')
            user.email = email
        user.nickname = nickname
        db.session.commit()
        flash('User profile updated successfully!', 'success')

    return render_template('foreground/accounts/edit_profile.html', card=card)


@mall_bp.route('/update_password', methods=['POST'])
def update_password():
    user = User.query.get(g.user.id)
    old_pwd = request.form.get('old_pwd')
    flag = check_password_hash(user.password, old_pwd)
    if flag:
        new_pwd = request.form.get('new_pwd')
        re_new_pwd = request.form.get('re_new_pwd')
        if new_pwd == re_new_pwd:
            user.password = generate_password_hash(new_pwd)
            db.session.commit()
            flash('Password updated successfully!', 'success')
        else:
            flash('The two passwords are different!', 'danger')
    else:
        flash('Old password verification error!', 'danger')
    return redirect(url_for('mall.edit_profile'))


@mall_bp.route('/add_card', methods=['POST'])
def add_card():
    card_number = request.form.get('card_number')
    card_name = request.form.get('card_name')
    card_exp = request.form.get('card_exp')
    card_cw = request.form.get('card_cw')
    postal_code = request.form.get('postal_code')
    card_obj = BankCardInfo()
    card_obj.card_number = card_number
    card_obj.card_name = card_name
    card_obj.card_exp = card_exp
    card_obj.card_cw = card_cw
    card_obj.user_id = g.user.id
    db.session.add(card_obj)
    db.session.commit()
    flash('Bank card payment added successfully!', 'success')
    return redirect(url_for('mall.edit_profile'))


@mall_bp.route('/del_card', methods=['GET'])
def del_card():
    card_id = request.args.get('card_id')
    card_obj = BankCardInfo.query.filter_by(user_id=g.user.id, id=card_id).first()
    if card_obj:
        db.session.delete(card_obj)
        db.session.commit()
        flash('Bank card deleted successfully!', 'success')
    else:
        flash('Bank card deletion failed!', 'danger')
    return redirect(url_for('mall.edit_profile'))


@mall_bp.route('/group_deals_list')
def group_deals_list():
    sql = Product.query.filter_by(product_type_id=1).order_by(Product.created_at.desc())
    page_data = sql.all()
    # page = int(request.args.get('page', 1))
    # page_data = sql.paginate(page=page, per_page=12).items
    count = sql.count()

    return render_template('foreground/goods/groupdeals_list.html', page_data=page_data, count=count)


@mall_bp.route('/group_deals_detail', methods=['GET'])
def group_deals_detail():
    pid = request.args.get('pid')
    if pid == '':
        flash('该商品不存在', 'danger')
        return redirect(url_for('mall.group_deals_list'))
    product_obj = Product.query.get(pid)

    i_list = []
    v_list = []

    for i_item in product_obj.product_image:
        i_list.append(i_item.img_path)
    for v_item in product_obj.product_video:
        v_list.append(v_item.video_path)
    media_count = len(i_list) + len(v_list)

    recommend = Product.query.filter(Product.product_type_id == 1, Product.status == 'APPROVED').order_by(Product.created_at.desc()).limit(2)

    return render_template('foreground/goods/groupdeals_detail.html', product_obj=product_obj, i_list=i_list, v_list=v_list, media_count=media_count, recommend=recommend)



@mall_bp.route('/index')
@mall_bp.route('/')
def index():
    product_obj = Product.query.filter(Product.product_type_id == 1, or_(Product.status == 'APPROVED', Product.status == 'FINISH')).order_by(Product.created_at.desc()).limit(4)

    return render_template('foreground/index.html', product_obj=product_obj)
