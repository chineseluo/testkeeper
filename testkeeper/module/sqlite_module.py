#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 19:39
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : sqlite_module.py
@IDE     : PyCharm
------------------------------------
"""
import json
from loguru import logger
from sqlalchemy import event

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import db.Column, db.String, db.Integer, DateTime, Text, Table, db.ForeignKey, db.BOOLEAN
# from sqlalchemy.dialects.sqlite import *
# from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
# from sqlalchemy.orm import db.relationship, backref, sessionmaker
# from testkeeper.util.file_operation import FileOption
# db.Model = declarative_base()
from testkeeper.ext import db


class TestPlanTable(db.Model):
    __tablename__ = "test_plan_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    projectName = db.Column(db.String(100), nullable=False)
    planName = db.Column(db.String(100), nullable=False)
    createUser = db.Column(db.String(100), nullable=True)
    cron = db.Column(db.String(100), nullable=False)
    isConfigMessagePush = db.Column(db.BOOLEAN, nullable=False)
    messagePushMethod = db.Column(db.String(500), nullable=False)
    messagePushWebhook = db.Column(db.String(500), nullable=False)
    enabled = db.Column(db.Boolean, nullable=True)  # 启用/禁用
    createBy = db.Column(db.String(100), nullable=True)  # 创建者
    updateBy = db.Column(db.String(100), nullable=True)  # 修改者
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)
    testJobs = db.relationship("TestJobTable", back_populates="testPlan", cascade="all,delete,delete-orphan",
                               passive_deletes=True)

    def __repr__(self):
        test_plan_table_dict = {
            "planId": self.id,
            "projectName": self.projectName,
            "planName": self.planName,
            "createUser": self.createUser,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePushMethod,
            "messagePushWebhook": self.messagePushWebhook,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return test_plan_table_dict

    def __str__(self):
        test_plan_table_dict = {
            "planId": self.id,
            "projectName": self.projectName,
            "planName": self.planName,
            "createUser": self.createUser,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePushMethod,
            "messagePushWebhook": self.messagePushWebhook,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return json.dumps(test_plan_table_dict)

    def to_dict(self):
        test_plan_table_dict = {
            "id": self.id,
            "projectName": self.projectName,
            "planName": self.planName,
            "createUser": self.createUser,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePushMethod,
            "messagePushWebhook": self.messagePushWebhook,
            "enabled": self.enabled,
            "createBy": self.createBy,
            "updateBy": self.updateBy,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return test_plan_table_dict

    @staticmethod
    def get_key_map():
        map_data = {
            "id": "id",
            "projectName": "projectName",
            "planName": "planName",
            "createUser": "createUser",
            "cron": "cron",
            "isConfigMessagePush": "isConfigMessagePush",
            "messagePushMethod": "messagePushMethod",
            "messagePushWebhook": "messagePushWebhook",
            "enabled": "enabled",
            "createBy": "createBy",
            "updateBy": "updateBy",
            "updateTime": "updateTime",
            "createTime": "createTime"
        }
        return map_data

    def from_dict(self, data):
        for field in ['id', 'projectName', "planName", "createUser",
                      'cron', 'isConfigMessagePush', 'messagePushMethod', 'messagePushWebhook', 'enabled',
                      'createBy', 'updateBy', 'updateTime', 'createTime']:
            if field in data:
                setattr(self, field, data[field])


class TestJobTable(db.Model):
    __tablename__ = "test_job_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    planId = db.Column(db.Integer, db.ForeignKey(TestPlanTable.id, ondelete="CASCADE"))
    jobName = db.Column(db.String(100), nullable=False)
    createUser = db.Column(db.String(100), nullable=False)
    executeScriptPath = db.Column(db.String(500), nullable=False)
    executeScriptCmd = db.Column(db.String(500), nullable=False)
    executeTimeout = db.Column(db.Integer, nullable=False, default=600)
    runFailedIsNeedContinue = db.Column(db.BOOLEAN, nullable=False)
    isSkipped = db.Column(db.BOOLEAN, nullable=False)
    checkInterval = db.Column(db.Integer, nullable=False, default=10)
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)
    testPlan = db.relationship(TestPlanTable, back_populates="testJobs")
    executeMachineIpList = db.relationship("TestMachineTable", back_populates="testJob",
                                           cascade="all,delete,delete-orphan")

    def __repr__(self):
        test_job_table_dict = {
            "jobId": self.id,
            "planId": self.planId,
            "jobName": self.jobName,
            "createUser": self.createUser,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "executeTimeout": self.executeTimeout,
            "isSkipped": self.isSkipped,
            "checkInterval": self.checkInterval,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return test_job_table_dict

    def __str__(self):
        test_job_table_dict = {
            "jobId": self.id,
            "planId": self.planId,
            "jobName": self.jobName,
            "createUser": self.createUser,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "isSkipped": self.isSkipped,
            "checkInterval": self.checkInterval,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return json.dumps(test_job_table_dict)

    def to_dict(self):
        test_job_table_dict = {
            "id": self.id,
            "planId": self.planId,
            "jobName": self.jobName,
            "createUser": self.createUser,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "isSkipped": self.isSkipped,
            "checkInterval": self.checkInterval,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return test_job_table_dict

    @staticmethod
    def get_key_map():
        test_job_table_dict = {
            "id": "jobId",
            "planId": "planId",
            "jobName": "jobName",
            "createUser": "createUser",
            "executeScriptPath": "executeScriptPath",
            "executeScriptCmd": "executeScriptCmd",
            "isSkipped": "isSkipped",
            "checkInterval": "checkInterval",
            "runFailedIsNeedContinue": "runFailedIsNeedContinue",
            "updateTime": "updateTime",
            "createTime": "createTime"
        }
        return test_job_table_dict

    def from_dict(self, data):
        for field in ['id', 'planId', "jobName", "createUser",
                      'executeScriptPath', 'executeScriptCmd', 'isSkipped', 'checkInterval', 'runFailedIsNeedContinue',
                      'createBy', 'updateBy', 'updateTime', 'createTime']:
            if field in data:
                setattr(self, field, data[field])


class TestPlanStatusTable(db.Model):
    __tablename__ = "test_plan_status_table"
    planId = db.Column(db.Integer, nullable=False)
    planName = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    executeStatus = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)
    testJobStatusList = db.relationship("TestJobStatusTable", back_populates="testPlanStatus")

    def __str__(self):
        test_plan_status_table_dict = {
            "planStatusId": self.id,
            "planId": self.planId,
            "planName": self.planName,
            "executeStatus": self.executeStatus,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return json.dumps(test_plan_status_table_dict)

    def __repr__(self):
        test_plan_status_table_dict = {
            "planStatusId": self.id,
            "planId": self.planId,
            "planName": self.planName,
            "executeStatus": self.executeStatus,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return test_plan_status_table_dict

    def to_dict(self):
        test_plan_status_table_dict = {
            "id": self.id,
            "planId": self.planId,
            "planName": self.planName,
            "executeStatus": self.executeStatus,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return test_plan_status_table_dict

    @staticmethod
    def get_key_map():
        test_job_table_dict = {
            "id": "planStatusId",
            "planId": "planId",
            "planName": "planName",
            "executeStatus": "executeStatus",
            "updateTime": "updateTime",
            "createTime": "createTime"
        }
        return test_job_table_dict

    def from_dict(self, data):
        for field in ['id', 'planId', "planName", "executeStatus",
                      'createBy', 'updateBy', 'updateTime', 'createTime']:
            if field in data:
                setattr(self, field, data[field])


class TestJobStatusTable(db.Model):
    __tablename__ = "test_job_status_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobId = db.Column(db.Integer, nullable=False)
    jobName = db.Column(db.String(100), nullable=False)
    planStatusId = db.Column(db.String(100), db.ForeignKey("test_plan_status_table.id"))
    executeStatus = db.Column(db.String(100), nullable=False)
    executeMachineIp = db.Column(db.String(100), nullable=False)
    processPid = db.Column(db.Integer, nullable=False)
    logFilePath = db.Column(db.String(100), nullable=False)
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)
    testPlanStatus = db.relationship("TestPlanStatusTable", back_populates="testJobStatusList")

    def __str__(self):
        test_job_status_table_dir = {
            "jobStatusId": self.id,
            "jobId": self.jobId,
            "jobName": self.jobName,
            "planStatusId": self.planStatusId,
            "processPid": self.processPid,
            "executeStatus": self.executeStatus,
            "executeMachineIp": self.executeMachineIp,
            "logFilePath": self.logFilePath,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return json.dumps(test_job_status_table_dir)

    def __repr__(self):
        test_job_status_table_dir = {
            "jobStatusId": self.id,
            "jobId": self.jobId,
            "jobName": self.jobName,
            "planStatusId": self.planStatusId,
            "processPid": self.processPid,
            "executeStatus": self.executeStatus,
            "executeMachineIp": self.executeMachineIp,
            "logFilePath": self.logFilePath,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return test_job_status_table_dir


class TestMachineTable(db.Model):
    # TODO 增加一个机器资源自动采集功能
    __tablename__ = "test_machine_table"
    machineId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobId = db.Column(db.String(100), db.ForeignKey("test_job_table.id"))
    ip = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    hostName = db.Column(db.String(100), nullable=True)
    cpuSize = db.Column(db.String(100), nullable=True)
    memorySize = db.Column(db.String(100), nullable=True)
    diskSize = db.Column(db.String(100), nullable=True)
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)
    testJob = db.relationship("TestJobTable", back_populates="executeMachineIpList")

    def __str__(self):
        test_machine_table_dict = {
            "machineId": self.machineId,
            "jobId": self.jobId,
            "username": self.username,
            "password": self.password,
            "hostName": self.hostName,
            "cpuSize": self.cpuSize,
            "memorySize": self.memorySize,
            "diskSize": self.diskSize,
            "updateTime": self.updateTime,
            "createTime": self.createTime
        }
        return json.dumps(test_machine_table_dict)

    def __repr__(self):
        test_machine_table_dict = {
            "machineId": self.machineId,
            "jobId": self.jobId,
            "username": self.username,
            "password": self.password,
            "hostName": self.hostName,
            "cpuSize": self.cpuSize,
            "memorySize": self.memorySize,
            "diskSize": self.diskSize,
            "updateTime": self.updateTime,
            "createTime": self.createTime
        }
        return test_machine_table_dict


class User(db.Model):
    __tablename__ = "user_info_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userName = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)


class Watcher(db.Model):
    __tablename__ = "plan_watcher"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plan_id = db.Column(db.Integer, nullable=True)  # plan id
    task_type = db.Column(db.String(100), nullable=True)  # 数据语句操作类型，update/insert/delete
    createTime = db.Column(db.TIMESTAMP, nullable=False)


@event.listens_for(TestPlanTable, 'after_insert', raw=True)
def watcher_plan_table_insert(mapper, connection, target):
    # {"planId": 6, "projectName": "\u6d4b\u8bd5\u9879\u76ee31", "planName": "\u6d4b\u8bd5\u8ba1\u52121", "createUser": "\u6210\u90fd-\u963f\u6728\u6728", "isScheduledExecution": true, "cron": "2 3 4 9 6", "isConfigMessagePush": true, "messagePushMethod": "\u4f01\u4e1a\u5fae\u4fe1", "messagePushWebhook": "www.baidu.com", "updateTime": "2023-04-12 11:48:23.655226", "createTime": "2023-04-12 11:48:23.655227"}
    logger.info(f"测试计划表planTable写入数据:{target.__dict__['_strong_obj']}")
    for item in target.__dict__:
        logger.info(item)
        logger.info(target.__dict__[item])
    logger.info("数据发生变更")


@event.listens_for(TestPlanTable, 'after_update', raw=True)
def watcher_plan_table_update(mapper, connection, target):
    logger.info(f"测试计划表planTable修改数据:{target.__dict__['_strong_obj']}")
    for item in target.__dict__:
        logger.info(item)
        logger.info(target.__dict__[item])
    logger.info("数据发生变更")


@event.listens_for(TestPlanTable, 'before_delete', raw=True)
def watcher_plan_table_delete(mapper, connection, target):
    logger.info("@@@@@@@@@@@")
    # logger.info(f"测试计划表planTable删除数据:{target.__dict__['_strong_obj']}")
    for item in target.__dict__:
        logger.info(item)
        logger.info(target.__dict__[item])
    logger.info("数据发生变更")

# @event.listens_for(db, "after_cursor_execute")
# def after_cursor_execute(conn, cursor, statement,
#                         parameters, context, executemany):
#     total = time.time() - conn.info['query_start_time'].pop(-1)
#     logger.debug("Query Complete!")


# if __name__ == '__main__':
#     db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
#     FileOption().create_dir(db_path)
#     db_name = "testkeeper.db"
#     sql = SQLalchemyDbOperation(db_path, db_name)
#     sql.create_table()
#     db.Model.metadata.create_all(sql.sqlalchemy_engine)
