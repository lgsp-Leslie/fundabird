#!/usr/bin/env python3
# coding=utf-8
# Version:python3.6.1
# File:views.py
# Author:LGSP_Harold
from io import BytesIO

from flask import Blueprint, make_response, session, request, jsonify, render_template, g, redirect, url_for, flash

from apps.models.mall_models import User
from apps.models.manage_models import Admin
from apps.utils.utils import get_verify_code, sms_send

# from models import Admin
from config import constants
from config.exts import cache, db

utils_bp = Blueprint('utils', __name__)

# 钩子函数,检查是否登录账号
required_login_list = ['/mall/edit_profile']


@utils_bp.before_app_request
def before_request():
    uid = session.get('uid')
    token = session.get('token')
    if not uid or not token:
        if request.path in required_login_list:
            return redirect(url_for('mall.login'))
        else:
            g.user = None
    else:
        if request.path in required_login_list:
            try:
                cache_set_value = cache.get(str(uid))
                if token not in cache_set_value:
                    session.clear()
                    g.user = None
                    return redirect(url_for('mall.login'))
                else:
                    user = User.query.get(uid)
                    # g对象，本次请求的对象
                    g.user = user
            except Exception as e:
                print('************', e)  # argument of type 'NoneType' is not iterable
                session.clear()
                g.user = None
                # flash('Your token has expired, please login again!', 'danger')
                return redirect(url_for('mall.login'))
        else:
            user = User.query.get(uid)
            # g对象，本次请求的对象
            g.user = user


# 登录验证码
@utils_bp.route('/verify_code')
def get_code():
    image, code = get_verify_code()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    # 将验证码字符串储存在session中
    session['verify_code'] = code
    return response


# 验证邮箱
@utils_bp.route('/confirm')
def confirm():
    user_id = request.args.get('user_id')
    token = request.args.get('token')
    user_obj = User.query.get(int(user_id))
    if user_obj.email_status == 'EMAIL_ACTIVE':
        flash('Your email has been verified. There is no need to click again!', 'success')
    else:
        try:
            if cache.get(str('confirm_' + str(user_id))) == token:
                flash('Your email has been verified!', 'success')
                user_obj.email_status = constants.EmailStatus.EMAIL_ACTIVE
                db.session.commit()
                cache.delete(str('confirm_' + str(user_id)))
            else:
                flash('Your email address verification failed. Please log in and resend the verification email!',
                      'danger')
        except Exception as e:
            flash('Your email verification has expired. Please resend the verification email!', 'danger')

    return redirect(url_for('mall.login'))


# 格式化银行卡号
@utils_bp.app_template_filter()
def card_number_format(card_number):
    card_number = str(card_number)
    return card_number[-4:-1]


# @utils_bp.route('/send_msg')
# def send_msg():
#     verify_code = session.get('verify_code')
#     verify_code = verify_code.lower()
#     input_verify_code = request.args.get('verify_code')
#     input_verify_code = input_verify_code.lower()
#     if verify_code != input_verify_code:
#         return jsonify(code=406, msg='验证码错误')
#     mobile_num = str(request.args.get('mobile').strip())
#     sms_code = 1111
#     session['mobile'] = mobile_num
#     session['check_code'] = sms_code
#     cache.set(mobile_num + '_sms', sms_code, timeout=600)
#     return jsonify(code=200, msg='短信发送成功')
# ——————————————————————
# json_result = sms_send(mobile_num)
# if json_result is not None:
#     if json_result['code'] == 200:
#         # msg字段表示此次短信发送的sendid；obj字段表示此次发送的验证码
#         send_id = json_result['msg'].strip()
#         check_code = json_result['obj'].strip()
#         session['send_id'] = send_id
#         session['phone'] = mobile_num
#         session['check_code'] = check_code
#         cache.set(mobile_num, check_code, timeout=600)
#         return jsonify(code=200, msg='短信发送成功', send_id=send_id)
#     else:
#         print(json_result)
#         return jsonify(code=json_result['code'], msg='短信发送失败')
