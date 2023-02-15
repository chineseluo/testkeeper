#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:11
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : __init__.py
@IDE     : PyCharm
------------------------------------
"""
from flask import Blueprint

menu_blue = Blueprint("menu", __name__, url_prefix="/api/menus")
from . import views