#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 18:24
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : users.py
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


@api_blue.route("/users", methods=["GET", "DELETE"])
def users_opt():
    if request.method == "GET":
        page = request.args["page"]
        size = request.args["size"]
        sort = request.args["sort"]
        dept_id = request.args.get("deptId", None)
        content_dict = {
            "content": []
        }
        users = SysUser.query.all() if dept_id is None else SysUser.query.filter_by(dept_id=dept_id).all()
        if len(users) != 0:
            for user in users:
                content_dict["content"].append(user.__repr__())
        content_dict.update({"totalElements": len(users)})
        return content_dict
    if request.method == "DELETE":
        user_ids = request.json
        for user_id in user_ids:
            SysUser.delete_by_user_id(user_id)
            logger.info(f"删除用户ID:{user_id}成功")
        return "SUCCESS"
