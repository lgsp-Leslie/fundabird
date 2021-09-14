#!/usr/bin/env python3
# coding=utf-8
# Version:python3.6.1
# File:utils.py
# Author:LGSP_Harold
import hashlib
import os
import random
import string
import uuid
from datetime import datetime
from time import time

from flask import render_template
from flask_mail import Message
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import requests
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from qiniu import put_data
from config.conf import Config
from config.exts import mail, cache


# 绘制验证码
def random_color():
    """ 随机颜色 """
    return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)


def gene_text():
    """ 生成4位验证码 """
    return ''.join(random.sample(string.ascii_letters + string.digits, 4))


def draw_lines(draw, num, width, height):
    """ 划干扰线 """
    for num in range(num):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)


def get_verify_code():
    """ 生成图形验证码 """
    code = gene_text()
    # 图片大小120×34
    width, height = 120, 34
    # 新图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 字体
    font = ImageFont.truetype('app/static/arial.ttf', 21)
    # draw对象
    draw = ImageDraw.Draw(im)
    # 绘制字符串
    for item in range(4):
        draw.text((5 + random.randint(-3, 3) + 23 * item, 3 + random.randint(-3, 3)),
                  text=code[item], fill=random_color(), font=font)
    # 划线
    draw_lines(draw, 2, width, height)
    # 高斯模糊
    im = im.filter(ImageFilter.GaussianBlur(radius=0.9))
    return im, code


# 发送短信
def sms_send(phone):
    url = Config.API_URL
    data = {
        'mobile': phone,  # 你的手机号码
    }
    app_secret = str(Config.APP_SECRET)
    app_key = str(Config.APP_KEY)
    # json类型
    nonce = str(Config.NONCE)  # 这个字符串时随机的长度不大于128
    cur_time = str(int((time() * 1000)))  # 采用时间戳
    content = app_secret + nonce + cur_time
    check_sum = hashlib.sha1(content.encode()).hexdigest()  # 对上述进行按要求哈希
    headers = {  # 设置请求头
        'AppKey': app_key,
        'Nonce': nonce,
        'CurTime': cur_time,
        'CheckSum': check_sum
    }
    try:
        response = requests.post(url, data=data, headers=headers)  # 发送post请求
        json_result = response.json()
        return json_result
    except Exception as e:
        print('调用API借口失败', str(e))


# 文件上传本地
def upload_file(file_storage, file_dir):
    # 如果不存在目录，则创建并授权
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        os.chmod(file_dir, 6)

    # 获取文件的名字
    file_name = file_storage.filename  # image_name.jpg
    # 重置为安全的文件名
    file_name = secure_filename(file_name)

    # splitext()分离文件名与扩展名
    file_info = os.path.splitext(file_name)
    # 获取扩展名并小写
    suffix = file_info[-1].lower()
    if suffix in Config.ALLOWED_EXTENSIONS:
        # 修改上传文件名称
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex) + suffix
        # file_path = file_dir + filename
        return filename
    else:
        return None


# 文件上传七牛云
def upload_qiniu(file_storage):
    # 获取上传文件的名字
    file_name = file_storage.filename  # image_name.jpg
    # 重置为安全的文件名
    file_name = secure_filename(file_name)

    # splitext()分离文件名与扩展名
    file_info = os.path.splitext(file_name)
    # 获取扩展名并小写
    suffix = file_info[-1].lower()

    if suffix in Config.ALLOWED_EXTENSIONS:
        # 生成不重复的文件名
        file_name = datetime.now().strftime('%Y%m%d%H%M%S') + str(uuid.uuid4().hex)
        # 重置为安全的文件名
        file_name = secure_filename(file_name)
        # 上传到七牛云保存的文件名
        key = file_name + suffix

        # 生成上传 Token，可以指定过期时间等
        token = Config.QINIU_Q.upload_token(Config.QINIU_BUCKET_NAME, key, 3600)

        # 通过二进制流上传到七牛
        ret, info = put_data(token, key, file_storage.read())
        return ret, info
    else:
        return None


# 删除七牛云的文件
def delete_qiniu(file_name):
    key = file_name
    ret, info = Config.QINIU_BUCKET.delete(Config.QINIU_BUCKET_NAME, key)
    return info


# 格式化手机号
def mobile_format(mobile):
    mobile = str(mobile)
    mobile = mobile.replace(mobile[3:8], '****')
    return mobile


# 发送邮件
def send_email(user_id, sender, subject, addressee, template,  **kwargs):
    msg = Message(subject, sender=sender, recipients=[addressee])
    token = generate_password_hash(str(user_id))
    cache.set(str('confirm_' + str(user_id)), token, timeout=259200)
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template, user_id=str(user_id), token=token, **kwargs)
    mail.send(msg)
