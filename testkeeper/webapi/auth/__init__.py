#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 16:17
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : __init__.py
@IDE     : PyCharm
------------------------------------
"""
from flask import Blueprint

auth_blue = Blueprint("auth", __name__, url_prefix="/auth")
from . import views
