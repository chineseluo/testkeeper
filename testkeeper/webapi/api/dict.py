#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 10:37
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : dict.py
@IDE     : PyCharm
------------------------------------
"""
from testkeeper.ext import db
from distutils.util import strtobool
import datetime
from sqlalchemy import and_, or_
from testkeeper.webapi.api import api_blue
from flask import Flask, jsonify, render_template, request, make_response, session
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysDict


@api_blue.route("/dict/", methods=["DELETE"])
@api_blue.route("/dict", methods=["GET", "POST", "DELETE", "PUT"])
def system_dict():
    if request.method == "GET":
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        sort = request.args.get("sort", None)
        blurry = request.args.get("blurry", None)
        sql_filter = []
        if sort:
            SORT_MAP = {
                "desc": {
                    "id": SysDict.dict_id.desc()
                },
                "asc": {
                    "id": SysDict.dict_id.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = SysDict.dict_id.asc()
        if blurry:
            like = SysDict.name.like(f"%{blurry}%")
            sql_filter.append(like)
        if page and size:
            offset = int(page) * int(size)
            sys_dicts = SysDict.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            sys_dicts = SysDict.query.filter(and_(*tuple(sql_filter))).order_by(order).all()
        return_dict = {
            "content": [sys_dict.to_dict() for sys_dict in sys_dicts],
            "totalElements": len(sys_dicts)
        }
        return return_dict

    if request.method in ["PUT", "POST"]:
        dict_json = request.json
        update_dict = {}
        for key in dict_json.keys():
            if key in SysDict.get_key_map().keys():
                if key == "createTime":
                    dict_json[key] = datetime.datetime.strptime(dict_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "updateTime":
                    dict_json[key] = datetime.datetime.strptime(dict_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                update_dict.update({SysDict.get_key_map()[key]: dict_json[key]})
        if request.method == "PUT":
            sys_dict = SysDict.query.filter_by(dict_id=dict_json['id']).first()
        else:
            sys_dict = SysDict()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_dict.create_time = NOW_TIME
            sys_dict.update_time = NOW_TIME
        sys_dict.from_dict(update_dict)
        db.session.add(sys_dict)
        db.session.commit()
        return "SUCCESS"

    if request.method == "DELETE":
        sys_dict_list = request.json
        for id in sys_dict_list:
            sys_dict = SysDict.query.get(id)
            db.session.delete(sys_dict)
            db.session.commit()
        return "SUCCESS"
