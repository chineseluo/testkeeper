#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:03
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : dept.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from io import BytesIO
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.webapi.api import api_blue
from testkeeper.util.image_operation import ImageCode
from testkeeper.util.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper


@api_blue.route("/dept", methods=["GET"])
def get_dept():
    sort = request.args["sort"]
    sys_depts = SysDept.query.order_by(SysDept.dept_id.desc()).all()
    return_dict = {
        "content": []
    }
    for dept in sys_depts:
        dept_dict = dept.__repr__()
        dept_dict.update({"leaf": False})
        dept_dict.update({"label": dept.name})
        dept_dict.update({"hasChildren": False})
        return_dict["content"].append(dept_dict)
    return_dict.update({"totalElements": len(sys_depts)})
    logger.info(return_dict)
    return return_dict
