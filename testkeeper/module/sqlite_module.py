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
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, DateTime, Text, Table, ForeignKey, BOOLEAN
from sqlalchemy.dialects.sqlite import *
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()


class TestPlanTable(Base):
    __tablename__ = "test_plan_table"
    planId = Column(Integer, primary_key=True, autoincrement=True)
    projectName = Column(String(100), nullable=False)
    testPlanName = Column(String(100), nullable=False)
    createUser = Column(String(100), nullable=True)
    isScheduledExecution = Column(BOOLEAN, nullable=False)
    cron = Column(String(100), nullable=False)
    isConfigMessagePush = Column(BOOLEAN, nullable=False)
    messagePushMethod = Column(String(500), nullable=False)
    messagePushWebhook = Column(String(500), nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testJobs = relationship("TestJobTable", back_populates="testPlan")

    def __repr__(self):
        test_plan_table_dict = {
            "planId": self.planId,
            "projectName": self.projectName,
            "testPlanName": self.testPlanName,
            "createUser": self.createUser,
            "isScheduledExecution": self.isScheduledExecution,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePushMethod,
            "messagePushWebhook": self.messagePushWebhook,
            "createTime": str(self.createTime)
        }
        return test_plan_table_dict

    def __str__(self):
        test_plan_table_dict = {
            "planId": self.planId,
            "projectName": self.projectName,
            "testPlanName": self.testPlanName,
            "createUser": self.createUser,
            "isScheduledExecution": self.isScheduledExecution,
            "cron": self.cron,
            "isConfigMessagePush": self.isConfigMessagePush,
            "messagePushMethod": self.messagePushMethod,
            "messagePushWebhook": self.messagePushWebhook,
            "createTime": str(self.createTime)
        }
        return json.dumps(test_plan_table_dict)


class TestJobTable(Base):
    __tablename__ = "test_job_table"
    jobId = Column(Integer, primary_key=True, autoincrement=True)
    planId = Column(String(100), ForeignKey('test_plan_table.planId'))
    jobName = Column(String(100), nullable=False)
    createUser = Column(String(100), nullable=False)
    executeMachineIpList = Column(String(500), nullable=False)
    executeStatus = Column(String(100), nullable=False)
    executeScriptPath = Column(String(500), nullable=False)
    executeScriptCmd = Column(String(500), nullable=False)
    executeTimeout = Column(Integer, nullable=False, default=600)
    runFailedIsNeedContinue = Column(BOOLEAN, nullable=False)
    isSkipped = Column(BOOLEAN, nullable=False)
    checkInterval = Column(Integer, nullable=False, default=10)
    createTime = Column(TIMESTAMP, nullable=False)
    testPlan = relationship("TestPlanTable", back_populates="testJobs")

    def __repr__(self):
        test_job_table_dict = {
            "planId": self.planId,
            "jobId": self.jobId,
            "jobName": self.jobName,
            "createUser": self.createUser,
            "executeMachineIpList": self.executeMachineIpList,
            "executeStatus": self.executeStatus,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "executeTimeout": self.executeTimeout,
            "isSkipped": self.isSkipped,
            "checkInterval": self.checkInterval,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "createTime": str(self.createTime)
        }
        return test_job_table_dict

    def __str__(self):
        test_job_table_dict = {
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
    userName = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    role = Column(String(100), nullable=True)
    phone = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    createTime = Column(TIMESTAMP, nullable=False)


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
    db_name = "testkeeper.db"
    sql = SQLalchemyDbOperation(db_path, db_name)
    sql.create_table()
    Base.metadata.create_all(sql.sqlalchemy_engine)
