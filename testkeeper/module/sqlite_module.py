#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 19:39
@Auth    : luozhongwen
@Email   : luozhongwen@sensorsdata.cn
@File    : sqlite_module.py
@IDE     : PyCharm
------------------------------------
"""
import json
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text, Table
from sqlalchemy.dialects.sqlite import *
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation

Base = declarative_base()


class TestPlanTable(Base):
    __tablename__ = "test_plan_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    planId = Column(String(100), nullable=False)
    projectName = Column(String(100), nullable=False)
    testPlanName = Column(String(100), nullable=False)
    createUser = Column(String(100), nullable=True)
    isScheduledExecution = Column(bool, nullable=False)
    cron = Column(String(100), nullable=False)
    isConfigMessagePush = Column(bool, nullable=False)
    messagePushMethod = Column(String(500), nullable=False)
    messagePushWebhook = Column(String(500), nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        test_plan_table_dict = {
            "id": self.id,
            "planId": self.planId,
            "projectName": self.projectName,
            "testPlanName": self.testPlanName,
            "createUser": self.createUser,
            "isScheduledExecution": self.isScheduledExecution,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePush,
            "messagePushWebhook": self.messagePushWebhook,
            "createTime": str(self.createTime)
        }
        return test_plan_table_dict

    def __str__(self):
        test_plan_table_dict = {
            "id": self.id,
            "planId": self.planId,
            "projectName": self.projectName,
            "testPlanName": self.testPlanName,
            "createUser": self.createUser,
            "isScheduledExecution": self.isScheduledExecution,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePush,
            "messagePushWebhook": self.messagePushWebhook,
            "createTime": str(self.createTime)
        }
        return json.dumps(test_plan_table_dict)


class TestJobTable(Base):
    __tablename__ = "test_job_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    planId = Column(String(100), nullable=False)
    jobId = Column(String(100), nullable=False)
    jobName = Column(String(100), nullable=False)
    createUser = Column(String(100), nullable=False)
    executeMachineIpList = Column(String(500), nullable=False)
    executeStatus = Column(String(100), nullable=False)
    executeScriptPath = Column(String(500), nullable=False)
    executeScriptCmd = Column(String(500), nullable=False)
    runFailedIsNeedContinue = Column(bool, nullable=False)
    isSkipped = Column(bool, nullable=False)
    checkInterval = Column(Integer, nullable=False, default=10)
    createTime = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        test_job_table_dict = {
            "id": self.id,
            "planId": self.planId,
            "jobId": self.jobId,
            "jobName": self.jobName,
            "createUser": self.createUser,
            "executeStatus": self.executeStatus,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "isSkipped": self.isSkipped,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "createTime": str(self.createTime)
        }
        return test_job_table_dict

    def __str__(self):
        test_job_table_dict = {
            "id": self.id,
            "planId": self.planId,
            "jobId": self.jobId,
            "jobName": self.jobName,
            "createUser": self.createUser,
            "executeStatus": self.executeStatus,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "isSkipped": self.isSkipped,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "createTime": str(self.createTime)
        }
        return json.dumps(test_job_table_dict)


class TestJobStatusTable(Base):
    __tablename__ = "test_job_status_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    jobId = Column(String(100), nullable=False)
    executeStatus = Column(String(100), nullable=False)
    executeMachineIp = Column(String(100), nullable=False)
    logFilePath = Column(String(100), nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)


class TestMachine(Base):
    # TODO 增加一个机器资源自动采集功能
    __tablename__ = "test_machine_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    jobId = Column(String(100), nullable=False)
    ip = Column(String(100), nullable=False)
    hostName = Column(String(100), nullable=True)
    cpu = Column(String(100), nullable=True)
    memory = Column(String(100), nullable=True)
    disk = Column(String(100), nullable=True)
    createTime = Column(TIMESTAMP, nullable=False)


class User(Base):
    __tablename__ = "user_info_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(Integer, primary_key=True, autoincrement=True)
    createTime = Column(TIMESTAMP, nullable=False)


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
    db_name = "testkeeper.db"
    sql = SQLalchemyDbOperation(db_path, db_name)
    sql.create_table()
    Base.metadata.create_all(sql.sqlalchemy_engine)
