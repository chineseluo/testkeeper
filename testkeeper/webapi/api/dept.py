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
import datetime
from distutils.util import strtobool
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.webapi.api import api_blue
from testkeeper.util.image_operation import ImageCode
from testkeeper.ext import db
from testkeeper.util.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper
from sqlalchemy import and_, or_


@api_blue.route("/dept", methods=["GET", "POST", "PUT", "DELETE"])
def dept():
    if request.method == "GET":
        sort = request.args.get("sort", None)

        page = request.args.get("page", None)
        size = request.args.get("size", None)
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        name = request.args.get("name", None)
        enabled = request.args.get("enabled", None)
        sql_filter = []
        SORT_MAP = {
            "desc": {
                "id": SysDept.dept_id.desc()
            },
            "asc": {
                "id": SysDept.dept_id.asc()
            }
        }
        if sort:
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = SysDept.dept_id.asc()
        if create_time_list:
            dept_create_time = SysDept.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(dept_create_time >= start_time)
            sql_filter.append(dept_create_time <= end_time)
        if enabled:
            sql_filter.append(SysDept.enabled == strtobool(enabled))
        if name:
            like = SysDept.name.like(f"%{name}%")
            sql_filter.append(like)
        if page and size:
            offset = int(page) * int(size)
            sys_depts = SysDept.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            sys_depts = SysDept.query.filter(and_(*tuple(sql_filter))).order_by(order).all()
        return_dict = {
            "content": [dept.to_dict() for dept in sys_depts],
            "totalElements": len(sys_depts)
        }
        return return_dict
    if request.method in ["POST", "PUT"]:
        dept_json = request.json
        update_dept = {}
        for key in dept_json.keys():
            if key in SysDept.get_key_map().keys():
                if key == "enabled":
                    if not isinstance(dept_json[key], bool):
                        dept_json[key] = strtobool(dept_json[key])
                if key == "createTime":
                    dept_json[key] = datetime.datetime.strptime(dept_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "updateTime":
                    dept_json[key] = datetime.datetime.strptime(dept_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                update_dept.update({SysDept.get_key_map()[key]: dept_json[key]})
        if request.method == "PUT":
            sys_dept = SysDept.query.filter_by(dept_id=dept_json['id']).first()
        else:
            sys_dept = SysDept()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_dept.create_time = NOW_TIME
            sys_dept.update_time = NOW_TIME
        sys_dept.from_dict(update_dept)
        db.session.add(sys_dept)
        db.session.commit()
        return "SUCCESS"
    if request.method == "DELETE":
        dept_id_list = request.json
        for id in dept_id_list:
            sys_dept = SysDept.query.get(id)
            db.session.delete(sys_dept)
            db.session.commit()
        return "SUCCESS"


@api_blue.route("/dept/superior", methods=["POST"])
def superior():
    req_json = request.json
    sys_depts = SysDept.query.all()
    return_dict = {
        "content": [dept.to_dict() for dept in sys_depts],
        "totalElements": len(sys_depts)
    }
    return return_dict
