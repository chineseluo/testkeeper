#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:52
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : menus.py
@IDE     : PyCharm
------------------------------------
"""
from sqlalchemy import and_
from testkeeper.ext import db
import datetime
from loguru import logger
from flask import Flask, jsonify, render_template, request, make_response, session
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysJob, SysMenu
from testkeeper.webapi.api import api_blue


@api_blue.route("/menus", methods=["POST", "GET", "DELETE", "PUT"])
def menus():
    if request.method == "GET":
        sort = request.args.get("sort", None)
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        blurry = request.args.get("blurry", None)
        pid = request.args.get("pid", None)
        sql_filter = []
        if sort:
            SORT_MAP = {
                "desc": {
                    "id": SysMenu.menu_id.desc()
                },
                "asc": {
                    "id": SysMenu.menu_id.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = SysMenu.menu_id.asc()
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        if create_time_list:
            meun_create_time = SysMenu.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(meun_create_time >= start_time)
            sql_filter.append(meun_create_time <= end_time)
        if blurry:
            like = SysMenu.name.like(f"%{blurry}%")
            sql_filter.append(like)
        sql_filter.append(SysMenu.pid == pid)
        if page and size:
            offset = int(page) * int(size)
            sys_menus = SysMenu.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            sys_menus = SysMenu.query.filter(and_(*tuple(sql_filter))).order_by(order).all()
        return_dict = {
            "content": [menu.to_dict() for menu in sys_menus],
            "totalElements": len(sys_menus)
        }
        return return_dict
    if request.method in ["POST", "PUT"]:
        ...

    if request.method == "DELETE":
        ...
