#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 16:19
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : views.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from io import BytesIO
from flask import Flask, jsonify, render_template, request, make_response, session
from testkeeper.webapi.auth import auth_blue
from testkeeper.util.image_operation import ImageCode


@auth_blue.route("/login", methods=["POST"])
def login():
    try:
        if request.method == "POST":
            print(request.json)
    except Exception as e:
        logger.info(e)


@auth_blue.route("/test/", methods=["GET"])
def test():
    logger.info("#########")
    return "test success"


@auth_blue.route("/code", methods=["GET"])
def code():
    image_code = ImageCode()
    image, code = image_code.getVerifyCode()
    # 图片以二进制形式写入
    buf = BytesIO()
    image.save(buf, 'png')
    buf_str = buf.getvalue()
    # response = make_response(buf_str)
    # response.headers['Content-Type'] = 'image/png'
    # session['imageCode'] = code
    # logger.info(code)
    test_dict = {
        "uuid": "test",
        "img": f"data:img/png;base64,{buf_str}"
    }
    return test_dict
