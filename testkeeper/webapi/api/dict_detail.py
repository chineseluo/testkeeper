#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:58
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : dictDict.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from io import BytesIO
import datetime
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.webapi.api import api_blue
from testkeeper.util.image_operation import ImageCode
from testkeeper.util.forms import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysDictDetail, SysDict, SysJob
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper
from sqlalchemy import and_
from testkeeper.ext import db


@api_blue.route("/dictDetail", methods=["GET", "PUT", "POST"])
def get_dict_detail():
    if request.method == "GET":
        dict_name = request.args.get("dictName", None)
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        sql_filter = []
        if dict_name:
            sys_dict = SysDict.query.filter_by(name=dict_name).first()
            logger.info(sys_dict.dict_id)
            sql_filter.append(SysDictDetail.dict_id == sys_dict.dict_id)
        if page and size:
            offset = int(page) * int(size)
            dict_details = SysDictDetail.query.filter(and_(*tuple(sql_filter))).offset(offset).limit(
                size).all()
        else:
            dict_details = SysDictDetail.query.filter(and_(*tuple(sql_filter))).all()
        return_dict = {
            "content": [dict_detail.to_dict() for dict_detail in dict_details],
            "totalElements": len(dict_details)
        }
        return return_dict
    if request.method in ["POST", "PUT"]:
        dict_detail_json = request.json
        update_dict_detail = {}
        for key in dict_detail_json.keys():
            if key in SysDictDetail.get_key_map().keys():
                update_dict_detail.update({SysDictDetail.get_key_map()[key]: dict_detail_json[key]})
            if key == "dict":
                update_dict_detail.update({SysDictDetail.get_key_map()["dict_id"]: dict_detail_json[key]["id"]})
        if request.method == "PUT":
            sys_dict_detail = SysDictDetail.query.filter_by(detail_id=dict_detail_json['id']).first()
        else:
            sys_dict_detail = SysDictDetail()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_dict_detail.create_time = NOW_TIME
            sys_dict_detail.update_time = NOW_TIME
        sys_dict_detail.from_dict(update_dict_detail)
        db.session.add(sys_dict_detail)
        db.session.commit()
        return "SUCCESS"

@api_blue.route("/dictDetail/<detail_id>", methods=["DELETE"])
def delete_dict_detail(detail_id):
    logger.info(detail_id)
    sys_dict_detail = SysDictDetail.query.get(detail_id)
    db.session.delete(sys_dict_detail)
    db.session.commit()
    return "SUCCESS"

