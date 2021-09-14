#!/usr/bin/env python3
# coding=utf-8
# File:__init__.py.py
# Author:LGSP_Harold
from datetime import datetime
from config.exts import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.now, comment='创建时间')
