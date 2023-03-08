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
import datetime
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
from testkeeper.ext import db


@api_blue.route("/job", methods=["GET", "DELETE", "POST", "PUT"])
def job_opt():
    if request.method == "GET":
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        offset = int(page) * int(size)

        sort = request.args.get("sort", None)
        sort_list = sort.split(",")
        SORT_MAP = {
            "desc": {
                "id": SysUser.user_id.desc()
            },
            "asc": {
                "id": SysUser.user_id.asc()
            }
        }
        enabled = request.args.get("enabled", None)
        name = request.args.get("name", None)
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        if not enabled:
            enabled = True if enabled == "true" else False
        sql_filter = []
        if enabled:
            sql_filter.append(SysUser.enabled == strtobool(enabled))
        if name:
            # 判断是邮箱还是名称
            like = SysUser.user_name.like(f"%{name}%") if not re.match(
                r'^[0-9a-za-z_]{0,19}@[0-9a-za-z]{1,13}\.[com,cn,net]{1,3}$', blurry) else SysUser.email.like(
                f"%{name}%")
            sql_filter.append(like)
        if create_time_list:
            user_create_time = SysJob.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(user_create_time >= start_time)
            sql_filter.append(user_create_time <= end_time)
        jobs = SysJob.query.all() if enabled is not None else SysJob.query.filter_by(enabled=bool(enabled)).all()
        job_content = {
            "content": [job.__repr__() for job in jobs],
            "totalElements": len(jobs)
        }
        return job_content
    if request.method in ["POST", "PUT"]:
        job_json = request.json
        update_job = {}
        for key in job_json.keys():
            if key in SysJob.get_key_map().keys():
                update_job.update({SysJob.get_key_map()[key]: job_json[key]})
        if request.method == "PUT":
            sys_job = SysJob.query.filter_by(user_id=job_json['id']).first()
        else:
            sys_job = SysJob()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_job.create_time = NOW_TIME
            sys_job.update_time = NOW_TIME
        sys_job.from_dict(update_job)
        db.session.add(sys_job)
        db.session.commit()
        return "SUCCESS"
    if request.method == "DELETE":
        job_id_list = request.json
        for id in job_id_list:
            sys_job = SysJob.query.get(id)
            db.session.delete(sys_job)
            db.session.commit()
        return "SUCCESS"
