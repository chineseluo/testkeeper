#!/user/bin/env python
# -*- coding: utf-8 -*-
import os
import json
from flask import Flask, jsonify
from loguru import logger
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from testkeeper.service.plan_service import PlanService
from testkeeper.module.sqlite_module import TestJobTable, TestPlanTable

app = Flask(__name__)
plan_service = PlanService()


class Config(object):
    DEBUG = True
    JSON_AS_ASCII = False


app.config.from_object(Config)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route("/job/update/")
def update_job_status():
    return 'update job status'


@app.route("/plan/job/start")
def start_job():
    return ""


@app.route("/plan/job/stop")
def stop_job():
    return ""


@app.route("/plan/job/delete")
def delete_job():
    return ""


@app.route("/plan/job/add")
def add_job():
    return ""


@app.route("/plan/job/get_job_status_list")
def get_job_status_list():
    return ""


@app.route("/plan/get_plan_list")
def get_test_plan_list():
    test_plan_list = plan_service.get_test_plan_list()
    return jsonify(test_plan_list)


@app.route("/plan/update")
def update_test_plan():
    return ""


@app.route("/plan/add")
def add_test_plan():
    return ""


@app.route("/plan/delete")
def delete_test_plan():
    return ""


if __name__ == '__main__':
    # app.config['JSON_AS_ASCII'] = False
    app.run()
