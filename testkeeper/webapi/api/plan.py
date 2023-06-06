from loguru import logger
from io import BytesIO
import datetime
from distutils.util import strtobool
import base64
from flask import Flask, jsonify, render_template, request, make_response, session
from flask_jwt_extended import create_access_token
from testkeeper.module.sqlite_module import TestPlanTable
from testkeeper.webapi.api import api_blue
from sqlalchemy import and_, or_
from testkeeper.ext import db


@api_blue.route("/plan", methods=["GET", "POST", "PUT", "DELETE"])
def plan():
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
                    "id": TestPlanTable.id.desc()
                },
                "asc": {
                    "id": TestPlanTable.id.asc()
                }
            }
            sort_list = sort.split(",")
            order = SORT_MAP[sort_list[1]][sort_list[0]]
        else:
            order = TestPlanTable.id.asc()
        if create_time_list:
            plan_create_time = TestPlanTable.createTime
            start_time = datetime.datetime.strptime(create_time_list[0], "%Y-%m-%d %H:%M:%S")
            end_time = datetime.datetime.strptime(create_time_list[1], "%Y-%m-%d %H:%M:%S")
            sql_filter.append(plan_create_time >= start_time)
            sql_filter.append(plan_create_time <= end_time)
        if enabled:
            sql_filter.append(TestPlanTable.enabled == strtobool(enabled))
        if name:
            like = TestPlanTable.planName.like(f"%{name}%")
            sql_filter.append(like)
        if page and size:
            offset = int(page) * int(size)
            sys_plans = TestPlanTable.query.filter(and_(*tuple(sql_filter))).order_by(order).offset(offset).limit(
                size).all()
        else:
            sys_plans = TestPlanTable.query.filter(and_(*tuple(sql_filter))).order_by(order).all()
        return_dict = {
            "content": [plan.to_dict() for plan in sys_plans],
            "totalElements": len(sys_plans)
        }
        return return_dict
    if request.method in ["POST", "PUT"]:
        plan_json = request.json
        logger.info(plan_json)
        update_plan = {}
        for key in plan_json.keys():
            if key in TestPlanTable.get_key_map().keys():
                if key == "enabled":
                    if not isinstance(plan_json[key], bool):
                        plan_json[key] = strtobool(plan_json[key])
                if key == "createTime":
                    plan_json[key] = datetime.datetime.strptime(plan_json[key], '%Y-%m-%d %H:%M:%S')
                if key == "updateTime":
                    plan_json[key] = datetime.datetime.strptime(plan_json[key], '%Y-%m-%d %H:%M:%S')
                if key == "isConfigMessagePush":
                    if not isinstance(plan_json[key], bool):
                        plan_json[key] = strtobool(plan_json[key])
                update_plan.update({TestPlanTable.get_key_map()[key]: plan_json[key]})
        if request.method == "PUT":
            sys_plan = TestPlanTable.query.filter_by(id=plan_json['id']).first()
        else:
            sys_plan = TestPlanTable()
            NOW_TIME = datetime.datetime.now().replace(microsecond=0)
            sys_plan.createTime = NOW_TIME
            sys_plan.updateTime = NOW_TIME
        sys_plan.from_dict(update_plan)
        db.session.add(sys_plan)
        db.session.commit()
        return "SUCCESS"
    if request.method == "DELETE":
        id_list = request.json
        for id in id_list:
            sys_plan = TestPlanTable.query.get(id)
            db.session.delete(sys_plan)
            db.session.commit()
        return "SUCCESS"
