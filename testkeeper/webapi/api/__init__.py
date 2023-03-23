#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:03
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : __init__.py
@IDE     : PyCharm
------------------------------------
"""
from flask import Blueprint

api_blue = Blueprint("api", __name__, url_prefix="/api")
from . import dept
from . import dict_detail
from . import users
from . import job
from . import roles
from . import dict
from . import menus
from . import server_deploy