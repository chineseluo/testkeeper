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
import datetime
import re
import time
from distutils.util import strtobool
from loguru import logger
import jsonpickle
from io import BytesIO
from testkeeper.ext import db
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
from sqlalchemy import or_, and_


@api_blue.route("/users", methods=["GET", "DELETE", "POST", "PUT"])
def users_opt():
    if request.method == "GET":
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        sort = request.args.get("sort", None)
        sort_list = sort.split(",")
        dept_id = request.args.get("deptId", None)
        enabled = request.args.get("enabled", None)
        # 搜索字段
        blurry = request.args.get("blurry", None)
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        sql_filter = []
        if dept_id:
            sql_filter.append(SysUser.dept_id == dept_id)
        if enabled:
            sql_filter.append(SysUser.enabled == strtobool(enabled))
        if blurry:
            # 判断是邮箱还是名称
            like = SysUser.user_name.like(f"%{blurry}%") if not re.match(
                r'^[0-9a-za-z_]{0,19}@[0-9a-za-z]{1,13}\.[com,cn,net]{1,3}$', blurry) else SysUser.email.like(
                f"%{blurry}%")
            sql_filter.append(like)
        if create_time_list:
            user_create_time = SysUser.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(user_create_time >= start_time)
            sql_filter.append(user_create_time <= end_time)
        SORT_MAP = {
            "desc": {
                "id": SysUser.user_id.desc()
            },
            "asc": {
                "id": SysUser.user_id.asc()
            }
        }
        offset = int(page) * int(size)
        users = SysUser.query.filter(and_(*tuple(sql_filter))).order_by(
            SORT_MAP[sort_list[1]][sort_list[0]]).offset(offset).limit(
            size).all()
        logger.info(users)
        content_dict = {
            "content": [user.to_dict() for user in users],
            "totalElements": len(users)
        }
        return content_dict
    if request.method == "DELETE":
        user_ids = request.json
        for user_id in user_ids:
            SysUser.delete_by_user_id(user_id)
            logger.info(f"删除用户ID:{user_id}成功")
        return "SUCCESS"
    if request.method in ["PUT", "POST"]:
        user_json = request.json
        update_user = {}
        for key in user_json.keys():
            if key in SysUser.get_key_map().keys():
                # 针对dept特殊处理一下
                if key == "dept":
                    user_json[key] = user_json[key]["id"]
                if key == "enabled":
                    if not isinstance(user_json[key], bool):
                        user_json[key] = strtobool(user_json[key])
                if key == "createTime":
                    user_json[key] = datetime.datetime.strptime(user_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "updateTime":
                    user_json[key] = datetime.datetime.strptime(user_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "pwdResetTime":
                    user_json[key] = datetime.datetime.strptime(user_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                update_user.update({SysUser.get_key_map()[key]: user_json[key]})
        jobs = [SysJob.query.filter_by(job_id=job['id']).first() for job in user_json["jobs"]]
        roles = [SysRole.query.filter_by(role_id=role['id']).first() for role in user_json["roles"]]
        if request.method == "PUT":
            sys_user = SysUser.query.filter_by(user_id=user_json['id']).first()
        else:
            sys_user = SysUser()
        sys_user.from_dict(update_user)
        sys_user.roles = roles
        sys_user.jobs = jobs
        db.session.add(sys_user)
        db.session.commit()
        return "SUCCESS"
