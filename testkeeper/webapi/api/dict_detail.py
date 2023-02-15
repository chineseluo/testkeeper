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
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysDictDetail, SysDict
from werkzeug.datastructures import ImmutableMultiDict
from testkeeper.util.decode_opeation import decryption
from functools import wraps, update_wrapper


@api_blue.route("/dictDetail", methods=["GET"])
def get_dict_detail():
    dict_name = request.args["dictName"]
    page = request.args["page"]
    pagesize = request.args["size"]
    # 查询SysDict获取Id list
    dict = SysDict.query.filter_by(name=dict_name).first()
    logger.info(dict)
    logger.info(dict.dict_id)
    # 根据dict_id 查询dictDetail信息
    dict_details = SysDictDetail.query.filter_by(dict_id=dict.dict_id).all()
    logger.info(dict_details)
    logger.info(dict_details[0].dict_id)
    return_dict = {
        "content": []
    }
    for dict_detail in dict_details:
        logger.info(dict_detail.dict_id)
        dict_detail_content = {
            "createTime": dict_detail.create_time,
            "dictSort": dict_detail.dict_sort,
            "id": dict_detail.detail_id,
            "label": dict_detail.label,
            "value": True,
            "dict": {
                "id": dict_detail.dict_id
            }
        }
        return_dict["content"].append(dict_detail_content)
    return_dict.update({"totalElements": len(dict_details)})
    return return_dict
