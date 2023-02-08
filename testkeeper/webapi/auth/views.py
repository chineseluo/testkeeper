#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 16:19
@Auth    : luozhongwen
@Email   : luozhongwen@sensorsdata.cn
@File    : views.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from flask import Flask, jsonify, render_template, request
from testkeeper.webapi.auth import auth_blue


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
