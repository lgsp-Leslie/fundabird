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
    nickname = db.Column(db.String(50), comment='昵称')
    password = db.Column(db.String(256), comment='密码')
    avatar = db.Column(db.String(256), comment='头像')
    donations = db.Column(db.Integer, default=0, comment='捐赠总额')
    coins = db.Column(db.Integer, default=0, comment='虚拟币$1=1')
    user_status = db.Column(db.Enum(constants.UserStatus), default=constants.UserStatus.USER_ACTIVE, comment='用户状态')
    email_status = db.Column(db.Enum(constants.EmailStatus), default=constants.EmailStatus.EMAIL_IN_ACTIVE,
                             comment='邮箱状态')
    online_status = db.Column(db.Enum(constants.OnlineStatus), default=constants.OnlineStatus.NOT_ONLINE,
                             comment='在线状态')
    user_role = db.Column(db.Enum(constants.UserRole), default=constants.UserRole.COMMON, comment='用户权限')
    bind_facebook = db.Column(db.String(50), unique=True, comment='Facebook邮箱绑定')
    user_login_type = db.Column(db.String(10), default='Fundabird', comment='用户登录类型')
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


class ProductTypes(BaseModel):
    # 商品类型表
    __tablename__ = 'mall_product_types'

    name = db.Column(db.String(50), nullable=False, comment='类型名称')


class ProductCategory(BaseModel):
    # 商品标签表
    __tablename__ = 'mall_product_category'

    name = db.Column(db.String(50), unique=True, nullable=False, comment='标签名称')


class ProductFaq(BaseModel):
    # 商品常见问题表
    __tablename__ = 'mall_product_faq'

    title = db.Column(db.String(80), nullable=False, comment='问题')
    desc = db.Column(db.String(512), nullable=False, comment='解答')

    product_id = db.Column(db.Integer, db.ForeignKey('mall_product.id'))
    product = db.relationship('Product', backref='product_faq')


class WishList(BaseModel):
    # 收藏列表
    __tablename__ = 'mall_wish_list'

    user_id = db.Column(db.Integer, db.ForeignKey('mall_user.id'))
    user = db.relationship('User', backref='wish_list')

    product_id = db.Column(db.Integer, db.ForeignKey('mall_product.id'))
    product = db.relationship('Product', backref='wish_list')


class ProductImage(BaseModel):
    # 商品图片表
    __tablename__ = 'mall_product_image'

    img_path = db.Column(db.String(256), comment='商品详情轮播图')
    product_id = db.Column(db.Integer, db.ForeignKey('mall_product.id'))
    product = db.relationship('Product', backref='product_image')


class ProductVideo(BaseModel):
    # 商品视频表
    __tablename__ = 'mall_product_video'

    video_path = db.Column(db.Text, comment='商品详情轮播视频')

    product_id = db.Column(db.Integer, db.ForeignKey('mall_product.id'))
    product = db.relationship('Product', backref='product_video')


class Product(BaseModel):
    # 商品表
    __tablename__ = 'mall_product'

    product_id = db.Column(db.String(128), nullable=False, comment='商品id，（团购：#GD-；创新：#IVP-；基金：#FD-。）')
    thumbnail = db.Column(db.String(256), comment='商品缩略图')
    title = db.Column(db.String(32), nullable=False, comment='商品标题')
    desc = db.Column(db.String(64), nullable=False, comment='商品简介')
    content = db.Column(db.Text, nullable=False)
    current_price = db.Column(db.Integer, nullable=False, comment='当前价格*100')
    historical_price = db.Column(db.Integer, comment='历史价格*100')
    discount = db.Column(db.Integer, comment='折扣0.1%')
    fluctuation_range = db.Column(db.Float, comment='涨跌幅0.01%')
    total = db.Column(db.Integer, nullable=False, comment='商品总数')
    sales_volume = db.Column(db.Integer, nullable=False, default=0, comment='销售量')
    start_time = db.Column(db.DateTime, nullable=False, comment='团购开始时间')
    end_time = db.Column(db.DateTime, nullable=False, comment='团购结束时间')
    status = db.Column(db.Enum(constants.ProductStatus), default=constants.ProductStatus.PENDING, comment='商品状态')
    status_flag = db.Column(db.SmallInteger, default=1, comment='状态标识：用来判断状态，减少查询')
    source = db.Column(db.String(20), comment='商品来源')
    give_coins = db.Column(db.Integer, default=0, comment='赠送的鸟币，最小单位多少？')

    product_category_id = db.Column(db.Integer, db.ForeignKey('mall_product_category.id'))
    product_category = db.relationship('ProductCategory', backref='product')

    product_type_id = db.Column(db.Integer, db.ForeignKey('mall_product_types.id'))
    product_type = db.relationship('ProductTypes', backref='product')

    user_id = db.Column(db.Integer, db.ForeignKey('mall_user.id'))
    user = db.relationship('User', backref='product')

    admin_id = db.Column(db.Integer, db.ForeignKey('manage_user.id'))
    admin = db.relationship('Admin', backref='product')


class Comment(BaseModel):
    # 评论回复表
    __tablename__ = 'mall_comment'

    comment = db.Column(db.String(1024), nullable=False, comment='评论')

    reply_id = db.Column(db.Integer, db.ForeignKey('mall_comment.id'))

    product_id = db.Column(db.Integer, db.ForeignKey('mall_product.id'))
    product = db.relationship('Product', backref='comment')

    user_id = db.Column(db.Integer, db.ForeignKey('mall_user.id'))
    user = db.relationship('User', backref='comment')

