from loguru import logger
from io import BytesIO
import datetime
from distutils.util import strtobool
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.module.sqlite_module import TestJobTable
from testkeeper.webapi.api import api_blue
from sqlalchemy import and_, or_
from testkeeper.ext import db


@api_blue.route("/task", methods=["GET", "POST", "PUT", "DELETE"])
def task():
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

        if sort:
            SORT_MAP = {
                "desc": {
                    "id": TestJobTable.id.desc()
                },
                "asc": {
                    "id": TestJobTable.id.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = TestJobTable.id.asc()
        if create_time_list:
            task_create_time = TestJobTable.createTime
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(task_create_time >= start_time)
            sql_filter.append(task_create_time <= end_time)
        if enabled:
            sql_filter.append(TestJobTable.enabled == strtobool(enabled))
        if name:
            like = TestJobTable.jobName.like(f"%{name}%")
            sql_filter.append(like)
        if page and size:
            offset = int(page) * int(size)
            sys_tasks = TestJobTable.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            sys_tasks = TestJobTable.query.filter(and_(*tuple(sql_filter))).order_by(order).all()
        return_dict = {
            "content": [task.to_dict() for task in sys_tasks],
            "totalElements": len(sys_tasks)
        }
        return return_dict
    if request.method in ["POST", "PUT"]:
        task_json = request.json
        logger.info(task_json)
        update_task = {}
        for key in task_json.keys():
            if key in TestJobTable.get_key_map().keys():
                if key == "enabled":
                    if not isinstance(task_json[key], bool):
                        task_json[key] = strtobool(task_json[key])
                if key == "createTime":
                    task_json[key] = datetime.datetime.strptime(task_json[key], '%Y-%m-%d %H:%M:%S')
                if key == "updateTime":
                    task_json[key] = datetime.datetime.strptime(task_json[key], '%Y-%m-%d %H:%M:%S')
                if key == "isConfigMessagePush":
                    if not isinstance(task_json[key], bool):
                        task_json[key] = strtobool(task_json[key])
                update_task.update({TestJobTable.get_key_map()[key]: task_json[key]})
        if request.method == "PUT":
            sys_task = TestJobTable.query.filter_by(id=task_json['id']).first()
        else:
            sys_task = TestJobTable()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_task.createTime = NOW_TIME
            sys_task.updateTime = NOW_TIME
        sys_task.from_dict(update_task)
        db.session.add(sys_task)
        db.session.commit()
        return "SUCCESS"
    if request.method == "DELETE":
        id_list = request.json
        for id in id_list:
            sys_task = TestJobTable.query.get(id)
            db.session.delete(sys_task)
            db.session.commit()
        return "SUCCESS"
