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
import re
import datetime
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.webapi.api import api_blue
from distutils.util import strtobool
from testkeeper.util.image_operation import ImageCode
from testkeeper.util.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysJob
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper
from testkeeper.ext import db
from sqlalchemy import and_


@api_blue.route("/job", methods=["GET", "DELETE", "POST", "PUT"])
def job_opt():
    if request.method == "GET":
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        offset = int(page) * int(size)
        enabled = request.args.get("enabled", None)
        name = request.args.get("name", None)
        sort = request.args.get("sort", None)
        # if "sort" in request.args.keys():
        #     sort_list = request.args.getlist("sort")
        #     sort_dict = {}
        #     for sort_index in range(0, len(sort_list)):
        #         sort_dict.update({"sort_": sort_list[sort_index].split(",")})
        if sort:
            SORT_MAP = {
                "desc": {
                    "id": SysJob.job_id.desc(),
                    "jobSort": SysJob.job_sort.desc()
                },
                "asc": {
                    "id": SysJob.job_id.asc(),
                    "jobSort": SysJob.job_sort.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = SysDept.dept_id.asc()
        sql_filter = []
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        if enabled:
            sql_filter.append(SysDept.enabled == strtobool(enabled))
        if name:
            # 判断是邮箱还是名称
            like = SysJob.name.like(f"%{name}%")
            sql_filter.append(like)
        if create_time_list:
            user_create_time = SysJob.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(user_create_time >= start_time)
            sql_filter.append(user_create_time <= end_time)
        if page and size:
            jobs = SysJob.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            jobs = SysJob.query.filter(and_(*tuple(sql_filter))).order_by(order).all()
        job_content = {
            "content": [job.to_dict() for job in jobs],
            "totalElements": len(jobs)
        }
        return job_content
    if request.method in ["POST", "PUT"]:
        job_json = request.json
        update_job = {}
        for key in job_json.keys():
            if key in SysJob.get_key_map().keys():
                if key == "createTime":
                    job_json[key] = datetime.datetime.strptime(job_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "updateTime":
                    job_json[key] = datetime.datetime.strptime(job_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                update_job.update({SysJob.get_key_map()[key]: job_json[key]})
        NOW_TIME = datetime.datetime.now().replace(microsecond=0)
        if request.method == "PUT":
            sys_job = SysJob.query.filter_by(job_id=job_json['id']).first()
        else:
            sys_job = SysJob()
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
