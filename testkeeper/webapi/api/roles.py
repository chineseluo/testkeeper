#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:39
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : roles.py
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
from sqlalchemy import and_
from testkeeper.ext import db


@api_blue.route("/roles/level", methods=["GET"])
def level_opt():
    return {"level": 1}


@api_blue.route("/roles/all", methods=["GET"])
def roles_opt():
    sys_roles = SysRole.query.all()
    sys_roles_list = [sys_role.__repr__() for sys_role in sys_roles]
    logger.info(sys_roles_list)
    return sys_roles_list


@api_blue.route("/roles", methods=["GET", "POST", "DELETE", "PUT"])
def roles_get():
    if request.method == "GET":
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        sort = request.args.get("sort", None)
        blurry = request.args.get("blurry", None)
        sql_filter = []
        if sort:
            SORT_MAP = {
                "desc": {
                    "level": SysRole.level.desc()
                },
                "asc": {
                    "level": SysRole.level.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = SysRole.level.asc()
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        if create_time_list:
            dept_create_time = SysRole.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(dept_create_time >= start_time)
            sql_filter.append(dept_create_time <= end_time)
        if blurry:
            like = SysRole.name.like(f"%{blurry}%")
            sql_filter.append(like)
        if page and size:
            logger.info("###")
            logger.info(sql_filter)
            offset = int(page) * int(size)
            sys_roles = SysRole.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            sys_roles = SysRole.query.filter(and_(*tuple(sql_filter))).order_by(order).all()

        roles_dict = {
            "content": [role.to_dict() for role in sys_roles],
            "totalElements": len(sys_roles)
        }
        return roles_dict
    if request.method in ["PUT", "POST"]:
        role_json = request.json
        update_role = {}
        for key in role_json.keys():
            if key in SysRole.get_key_map().keys():
                if key == "createTime":
                    role_json[key] = datetime.datetime.strptime(role_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "updateTime":
                    role_json[key] = datetime.datetime.strptime(role_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                update_role.update({SysRole.get_key_map()[key]: role_json[key]})
        if request.method == "PUT":
            sys_role = SysRole.query.filter_by(role_id=role_json['id']).first()
        else:
            sys_role = SysRole()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_role.create_time = NOW_TIME
            sys_role.update_time = NOW_TIME
        logger.info(update_role)
        sys_role.from_dict(update_role)
        logger.info(sys_role.to_dict())

        db.session.add(sys_role)
        db.session.commit()
        return "SUCCESS"

    if request.method == "DELETE":
        sys_roles_list = request.json
        for id in sys_roles_list:
            sys_role = SysRole.query.get(id)
            db.session.delete(sys_role)
            db.session.commit()
        return "SUCCESS"


@api_blue.route("/roles/menu", methods=["GET", "POST", "DELETE", "PUT"])
def roles_menu():
    ...
