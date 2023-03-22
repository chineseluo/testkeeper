#!/user/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import threading
from flask import Flask, jsonify, render_template, request

# sys.path.insert(0, "../")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from testkeeper.webapi.auth import auth_blue
from testkeeper.webapi.menu import menu_blue
from testkeeper.webapi.api import api_blue
from loguru import logger
from testkeeper.service.plan_service import PlanService
from testkeeper.builtin.task_scheduler import TaskScheduler
from flask_migrate import Migrate
from testkeeper.module.sys_user_module import init_data
from testkeeper.module.sys_user_module import *
from flask_jwt_extended import JWTManager


class FlaskApp(Flask):
    def __init__(self, *args, **kwargs):
        super(FlaskApp, self).__init__(*args, **kwargs)
    #     self._run_task_scheduler()
    #
    # @staticmethod
    # def _run_task_scheduler():
    #     ts = TaskScheduler()
    #     task_scheduler_thread = threading.Thread(target=ts.start_execute_time_job, args=())
    #     task_scheduler_thread.setDaemon(True)
    #     task_scheduler_thread.start()

    # @staticmethod
    # def _init_database_data():


class Config(object):
    DEBUG = True
    JSON_AS_ASCII = False

    DATABASE = 'testkeeper.db'
    DBPATH = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "testkeeper",
                          "db")
    DBURL = f'sqlite:///{os.path.join(DBPATH, DATABASE)}'
    SQLALCHEMY_DATABASE_URI = DBURL
    logger.info(DBURL)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


app = FlaskApp(__name__, static_folder="./templates/static", template_folder="./templates")
app.secret_key = "testkeeper.user@secret.key"
# 初始化配置
app.config.from_object(Config)
# 绑定APP
from testkeeper.ext import db

jwt = JWTManager(app)
db.init_app(app)
# 注册蓝图
app.register_blueprint(auth_blue)
app.register_blueprint(menu_blue)
app.register_blueprint(api_blue)
# 设置session过期时间
app.permanent_session_lifetime = datetime.timedelta(seconds=60*30)
# 初始化迁移框架
migrate = Migrate(app=app, db=db)
"""
migrate
初始化一个环境：python manage.py db init 只需要执行一次
自动检测模型，生成迁移脚本：python manage.py db migrate 识别ORM模型的改变，生成前迁移脚本
将迁移脚本映射到数据库中：python manage.py db upgrade  运行迁移脚本，同步到数据库中
更多命令：python manage.py db --help
rm -rf ./db/testkeeper.db && rm -rf ./migrations && flask db init && flask db migrate && flask db upgrade
"""
plan_service = PlanService()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def hello_world(path):
    return render_template("index.html")


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
    # print(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
    # DBPATH = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))),"testkeeper", "db")
    # print("###")
    # print(DBPATH)
    app.run(debug=True, threaded=True)

    # with app.app_context():
    #     init_data()
