#!/usr/bin/env python3
# coding=utf-8
# Author:LGSP_Harold
from datetime import datetime
from uuid import uuid4

from flask import Blueprint, session, redirect, url_for, g, request, flash, render_template, jsonify
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash

from apps.manage.forms import LoginForm
from apps.models.mall_models import User, ProductTypes, Product, ProductCategory, ProductVideo, ProductImage
from apps.models.manage_models import Admin
from apps.utils.utils import upload_file
from config import constants
from config.conf import Config
from config.exts import db

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
    return render_template('background/login.html', form=form)


@manage_bp.route('/index')
def index():
    return render_template('background/index.html')


@manage_bp.route('/user_list')
def user_list():
    page = int(request.args.get('page', 1))
    page_data = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('background/user_list.html', page_data=page_data)


@manage_bp.route('/user_detail')
def user_detail():
    uid = request.args.get('uid')
    user = User.query.get(uid)
    if user is None:
        flash('User does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.user_list'))
    return render_template('background/user_detail.html', user=user)


@manage_bp.route('/modify_user_status')
def modify_user_status():
    uid = request.args.get('uid')
    user = User.query.get(uid)
    if user is None:
        flash('User does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.user_list'))
    if user.user_status.value == 'Enable':
        user.user_status = constants.UserStatus.USER_IN_ACTIVE
        flash('User：' + str(user.id) + ',user status disabled successfully!', 'success')
    else:
        user.user_status = constants.UserStatus.USER_ACTIVE
        flash('User：' + str(user.id) + ',user status enabled successfully!', 'success')
    db.session.commit()
    return redirect(url_for('manage.user_list'))


@manage_bp.route('/del_user')
def del_user():
    uid = request.args.get('uid')
    user = User.query.get(uid)
    if user is None:
        flash('User does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.user_list'))
    db.session.delete(user)
    db.session.commit()
    flash('Success! User deleted!', 'success')
    return redirect(url_for('manage.user_list'))


@manage_bp.route('/admin_list')
def admin_list():
    page = int(request.args.get('page', 1))
    page_data = Admin.query.order_by(Admin.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('background/admin_list.html', page_data=page_data)


@manage_bp.route('/admin_detail')
def admin_detail():
    aid = request.args.get('aid')
    admin = Admin.query.get(aid)
    if admin is None:
        flash('Admin does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.admin_list'))
    return render_template('background/admin_detail.html', admin=admin)


@manage_bp.route('/modify_admin_status')
def modify_admin_status():
    aid = request.args.get('aid')
    admin = Admin.query.get(aid)
    if admin is None:
        flash('admin does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.admin_list'))
    if admin.user_status.value == 'Enable':
        admin.user_status = constants.UserStatus.USER_IN_ACTIVE
        flash('Admin：' + admin.username + ',user status disabled successfully!', 'success')
    else:
        admin.user_status = constants.UserStatus.USER_ACTIVE
        flash('Admin：' + admin.username + ',user status enabled successfully!', 'success')
    db.session.commit()
    return redirect(url_for('manage.admin_list'))


@manage_bp.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        admin_username = Admin.query.filter_by(username=username).first()
        if admin_username:
            flash('Username already exists', 'danger')
            return render_template('background/admin_add.html', form=form)
        admin = Admin()
        admin.username = username
        admin.password = generate_password_hash(password)
        db.session.add(admin)
        db.session.commit()
        flash('Administrator created successfully！', 'success')

    return render_template('background/admin_add.html', form=form)


@manage_bp.route('/del_admin')
def del_admin():
    aid = request.args.get('aid')
    admin = Admin.query.get(aid)
    if admin is None:
        flash('Admin does not exist, please refresh and try again!', 'danger')
        return redirect(url_for('manage.admin_list'))
    db.session.delete(admin)
    db.session.commit()
    flash('Success! Admin deleted!', 'success')
    return redirect(url_for('manage.admin_list'))


@manage_bp.route('/product_type_list')
def product_type_list():
    p_type = ProductTypes.query.all()
    return render_template('background/product_type_list.html', p_type=p_type)


@manage_bp.route('/add_product_type', methods=['GET', 'POST'])
def add_product_type():
    if request.method == 'POST':
        name = request.form.get('type_name')
        flag = ProductTypes.query.filter_by(name=name).first()
        if flag:
            flash('Commodity type name already exists!', 'danger')
            return redirect(url_for('manage.add_product_type'))
        product_type = ProductTypes()
        product_type.name = name
        db.session.add(product_type)
        db.session.commit()
        flash('Product type name added successfully!', 'success')
    return render_template('background/product_type_add.html')


@manage_bp.route('/group_deals_list')
def group_deals_list():
    page = int(request.args.get('page', 1))
    page_data = Product.query.filter_by(product_type_id=1).order_by(Product.created_at.desc()).paginate(page=page, per_page=Config.PER_PAGE)
    return render_template('background/product_group_deals_list.html', page_data=page_data)


def multiple_upload(file, prod_id):
    up_file_list = []
    file_name = upload_file(file, Config.UPLOADS_PROJECT_IMAGE_DIR)
    if file_name is not None:
        file_path = Config.UPLOADS_PROJECT_IMAGE_DIR + file_name
        file.save(file_path)
        up_file_list.append(Config.UPLOADS_PROJECT_IMAGE + file_name)
        product_image_obj = ProductImage()
        product_image_obj.img_path = up_file_list
        product_image_obj.product_id = prod_id
        db.session.add(product_image_obj)
    return up_file_list


@manage_bp.route('/add_product_group_deals', methods=['GET', 'POST'])
def add_product_group_deals():
    if request.method == 'POST':
        group = request.form.get('group')
        thumbnail = request.files.get('thumbnail')
        title = request.form.get('title')
        desc = request.form.get('desc')
        content = request.form.get('content')
        current_price = int(float(request.form.get('current_price')) * 100)
        historical_price = request.form.get('historical_price')
        total = request.form.get('total')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        coins = request.form.get('coins')
        source = request.form.get('source')
        category = request.form.get('category')
        video_path = request.form.get('video_path')

        files = request.files.getlist('images')
        product_id = 'GD-' + str(uuid4().hex) + datetime.now().strftime('%Y%m%d%H%M%S')
        product = Product()

        product.product_id = product_id
        if thumbnail:
            thumbnail_name = upload_file(thumbnail, Config.UPLOADS_THUMBNAIL_IMAGE_DIR)
            if thumbnail_name is not None:
                file_path = Config.UPLOADS_THUMBNAIL_IMAGE_DIR + thumbnail_name
                thumbnail.save(file_path)
                product.thumbnail = Config.UPLOADS_THUMBNAIL_IMAGE + thumbnail_name
            else:
                flash('缩略图不能为空!', 'danger')
                return redirect('manage.add_product_group_deals')

        product.title = title
        product.desc = desc
        product.content = content
        product.current_price = current_price
        if historical_price:
            historical_price = int(float(request.form.get('historical_price')) * 100)
            product.historical_price = historical_price
            discount = current_price / historical_price * 100
            product.discount = discount
        product.total = total
        product.start_time = start_time
        product.end_time = end_time
        product.give_coins = coins
        product.source = source
        if group == 'admin':
            # product.admin_id = g.user.id
            product.admin_id = 4
        else:
            # product.user_id = g.user.id
            product.user_id = 1
        if category != '':
            category_obj = ProductCategory.query.filter_by(name=category).first()
            if category_obj:
                product_category_id = category_obj.id
            else:
                product_category = ProductCategory()
                product_category.name = category
                db.session.add(product_category)
                db.session.commit()
                category_obj = ProductCategory.query.filter_by(name=category).first()
                product_category_id = category_obj.id
            product.product_category_id = product_category_id

        project_type_obj = ProductTypes.query.filter_by(name='Group Deals').first()
        project_type_id = project_type_obj.id
        product.product_type_id = project_type_id

        db.session.add(product)
        db.session.commit()

        product_obj = Product.query.filter_by(product_id=product_id).first()
        if files:
            for file in files:
                result = multiple_upload(file, product_obj.id)
                if not result:
                    flash('上传失败', 'danger')
                    return redirect(url_for('manage.add_product_group_deals'))

        if video_path:
            video_obj = ProductVideo()
            video_obj.video_path = video_path
            video_obj.product_id = product_obj.id
            db.session.add(video_obj)
        db.session.commit()

        flash('新增成功', 'success')
        return redirect(url_for('manage.group_deals_list'))

    return render_template('background/product_group_deals_add.html')


@manage_bp.route('/tiny_upload', methods=['POST'])
def tiny_upload():
    file = request.files['file']
    file_name = upload_file(file, Config.UPLOADS_PROJECT_IMAGE_DIR)
    if file_name is not None:
        file_path = Config.UPLOADS_PROJECT_IMAGE_DIR + file_name
        file.save(file_path)
        product_image_obj = ProductImage()
        up_file_path = Config.UPLOADS_PROJECT_IMAGE + file_name
        product_image_obj.img_path = up_file_path
        db.session.add(product_image_obj)
        db.session.commit()
        return jsonify(location=up_file_path)


@manage_bp.route('/innovation_products_list')
def innovation_products_list():
    pass


@manage_bp.route('/funding_products_list')
def funding_products_list():
    pass
