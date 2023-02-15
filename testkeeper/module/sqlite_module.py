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
    isScheduledExecution = db.Column(db.BOOLEAN, nullable=False)
    cron = db.Column(db.String(100), nullable=False)
    isConfigMessagePush = db.Column(db.BOOLEAN, nullable=False)
    messagePushMethod = db.Column(db.String(500), nullable=False)
    messagePushWebhook = db.Column(db.String(500), nullable=False)
    updateTime = db.Column(db.TIMESTAMP, nullable=False)
    createTime = db.Column(db.TIMESTAMP, nullable=False)
    testJobs = db.relationship("TestJobTable", back_populates="testPlan")

    def __repr__(self):
        test_plan_table_dict = {
            "planId": self.id,
            "projectName": self.projectName,
            "planName": self.planName,
            "createUser": self.createUser,
            "isScheduledExecution": self.isScheduledExecution,
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
            "isScheduledExecution": self.isScheduledExecution,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePushMethod,
            "messagePushWebhook": self.messagePushWebhook,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return json.dumps(test_plan_table_dict)


class TestJobTable(db.Model):
    __tablename__ = "test_job_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    planId = db.Column(db.String(100), db.ForeignKey('test_plan_table.id'))
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
    testPlan = db.relationship("TestPlanTable", back_populates="testJobs")
    executeMachineIpList = db.relationship("TestMachineTable", back_populates="testJob")

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


class TestPlanStatusTable(db.Model):
    __tablename__ = "test_plan_status_table"
    planId = db.Column(db.String(100), nullable=False)
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


class TestJobStatusTable(db.Model):
    __tablename__ = "test_job_status_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jobId = db.Column(db.String(100), nullable=False)
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

#
# @event.listens_for(TestPlanTable, 'after_insert', raw=True)
# @event.listens_for(TestPlanTable, 'after_update', raw=True)
# @event.listens_for(TestPlanTable, 'after_delete', raw=True)
# def watcher_plan_table_cron_change(mapper, connection, target):
#     logger.info(mapper)
#     logger.info(connection)
#     logger.info(target.dict['cron'])
#     logger.info(target.dict['isConfigMessagePush'])
#     logger.info(dir(target))
#     for item in target.__dict__:
#         logger.info(item)
#     logger.info("数据发生变更")


# if __name__ == '__main__':
#     db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
#     FileOption().create_dir(db_path)
#     db_name = "testkeeper.db"
#     sql = SQLalchemyDbOperation(db_path, db_name)
#     sql.create_table()
#     db.Model.metadata.create_all(sql.sqlalchemy_engine)
