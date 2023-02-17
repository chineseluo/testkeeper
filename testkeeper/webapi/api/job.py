#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:16
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : job.py
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
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysJob
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper


@api_blue.route("/job", methods=["GET", "DELETE"])
def job_opt():
    page = request.args.get("page")
    size = request.args.get("size")
    enable = request.args.get("enable")
    if not enable:
        enable = True if enable == "true" else False
    jobs = SysJob.query.all() if enable is not None else SysJob.query.filter_by(enable=bool(enable)).all()
    job_content = {
        "content": [job.__repr__() for job in jobs],
        "totalElements": len(jobs)
    }
    return job_content
