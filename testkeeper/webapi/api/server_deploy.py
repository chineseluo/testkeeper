#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:39
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : server_deploy.py
@IDE     : PyCharm
------------------------------------
"""
import datetime
from sqlalchemy import and_, or_
from loguru import logger
from testkeeper.webapi.api import api_blue
from flask import Flask, jsonify, render_template, request, make_response, session
from testkeeper.module.sys_user_module import SysUser, SysRole, SysUserRoles, SysDept, SysJob, MntServer
from testkeeper.ext import db


@api_blue.route("/serverDeploy", methods=["GET", "PUT", "POST", "DELETE"])
def server_deploy():
    if request.method == "GET":
        page = request.args.get("page", None)
        size = request.args.get("size", None)
        sort = request.args.get("sort", None)
        blurry = request.args.get("id", None)
        sql_filter = []
        if sort:
            SORT_MAP = {
                "desc": {
                    "id": MntServer.server_id.desc()
                },
                "asc": {
                    "id": MntServer.server_id.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = MntServer.server_id.asc()
        create_time_list = None
        if "createTime" in request.args.keys():
            create_time_list = request.args.getlist("createTime")
        if create_time_list:
            server_create_time = MntServer.create_time
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(server_create_time >= start_time)
            sql_filter.append(server_create_time <= end_time)
        if blurry:
            name_like = MntServer.name.like(f"%{blurry}%")
            ip_like = MntServer.ip.like(f"%{blurry}%")
            sql_filter.append(or_(name_like, ip_like))
            # sql_filter.append(ip_like)
        if page and size:
            logger.info("###")
            logger.info(sql_filter)
            offset = int(page) * int(size)
            mnt_servers = MntServer.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            mnt_servers = MntServer.query.filter(and_(*tuple(sql_filter))).order_by(order).all()

        servers_dict = {
            "content": [role.to_dict() for role in mnt_servers],
            "totalElements": len(mnt_servers)
        }
        return servers_dict

    if request.method in ["PUT", "POST"]:
        server_json = request.json
        update_server = {}
        for key in server_json.keys():
            if key in MntServer.get_key_map().keys():
                if key == "createTime":
                    server_json[key] = datetime.datetime.strptime(server_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                if key == "updateTime":
                    server_json[key] = datetime.datetime.strptime(server_json[key], '%a, %d %b %Y %H:%M:%S GMT')
                update_server.update({MntServer.get_key_map()[key]: server_json[key]})
        if request.method == "PUT":
            mnt_server = MntServer.query.filter_by(server_id=server_json['id']).first()
        else:
            mnt_server = MntServer()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            mnt_server.create_time = NOW_TIME
            mnt_server.update_time = NOW_TIME
        logger.info(update_server)
        mnt_server.from_dict(update_server)
        logger.info(mnt_server.to_dict())
        db.session.add(mnt_server)
        db.session.commit()
        return "SUCCESS"
    if request.method == "DELETE":
        mnt_server_list = request.json
        for id in mnt_server_list:
            mnt_server = MntServer.query.get(id)
            db.session.delete(mnt_server)
            db.session.commit()
        return "SUCCESS"

@api_blue.route("/serverDeploy/testConnect", methods=["POST"])
def test_connect():
    ...
