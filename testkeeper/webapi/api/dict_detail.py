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


@api_blue.route("/dictDetail", methods=["GET", "DELETE", "PUT", "POST"])
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
        job_json = request.json
        update_job = {}
        for key in job_json.keys():
            if key in SysJob.get_key_map().keys():
                update_job.update({SysJob.get_key_map()[key]: job_json[key]})
        if request.method == "PUT":
            sys_job = SysJob.query.filter_by(user_id=job_json['id']).first()
        else:
            sys_job = SysJob()
        sys_job.from_dict(update_job)
        db.session.add(sys_job)
        db.session.commit()
        return "SUCCESS"
    if request.method == "DELETE":
        job_json = request.json
        update_job = {}
        for key in job_json.keys():
            if key in SysJob.get_key_map().keys():
                update_job.update({SysJob.get_key_map()[key]: job_json[key]})
        if request.method == "PUT":
            sys_job = SysJob.query.filter_by(user_id=job_json['id']).first()
        else:
            sys_job = SysJob()
        sys_job.from_dict(update_job)
        db.session.add(sys_job)
        db.session.commit()
        return "SUCCESS"