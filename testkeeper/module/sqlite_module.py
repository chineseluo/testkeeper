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
    id = Column(Integer, primary_key=True, autoincrement=True)
    projectName = Column(String(100), nullable=False)
    planName = Column(String(100), nullable=False)
    createUser = Column(String(100), nullable=True)
    isScheduledExecution = Column(BOOLEAN, nullable=False)
    cron = Column(String(100), nullable=False)
    isConfigMessagePush = Column(BOOLEAN, nullable=False)
    messagePushMethod = Column(String(500), nullable=False)
    messagePushWebhook = Column(String(500), nullable=False)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testJobs = relationship("TestJobTable", back_populates="testPlan")

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


class TestJobTable(Base):
    __tablename__ = "test_job_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    planId = Column(String(100), ForeignKey('test_plan_table.id'))
    jobName = Column(String(100), nullable=False)
    createUser = Column(String(100), nullable=False)
    executeScriptPath = Column(String(500), nullable=False)
    executeScriptCmd = Column(String(500), nullable=False)
    executeTimeout = Column(Integer, nullable=False, default=600)
    runFailedIsNeedContinue = Column(BOOLEAN, nullable=False)
    isSkipped = Column(BOOLEAN, nullable=False)
    checkInterval = Column(Integer, nullable=False, default=10)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testPlan = relationship("TestPlanTable", back_populates="testJobs")
    testSteps = relationship("TestStepTable", back_populates="testJob")
    executeMachineIpList = relationship("TestMachineTable", back_populates="testJob")

    def __repr__(self):
        test_job_table_dict = {
            "planId": self.planId,
            "jobId": self.id,
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
            "planId": self.planId,
            "jobId": self.id,
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


class TestStepTable(Base):
    __tablename__ = "test_step_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    jobId = Column(String(100), ForeignKey('test_job_table.id'))
    stepName = Column(String(500), nullable=False)
    executeScriptPath = Column(String(500), nullable=False)
    executeScriptCmd = Column(String(500), nullable=False)
    runFailedIsNeedContinue = Column(BOOLEAN, nullable=False)
    isSkipped = Column(BOOLEAN, nullable=False)
    checkInterval = Column(Integer, nullable=False, default=10)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testJob = relationship("TestJobTable", back_populates="testSteps")

    def __repr__(self):
        test_step_table_dict = {
            "stepId": self.id,
            "jobId": self.jobId,
            "stepName": self.stepName,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "isSkipped": self.isSkipped,
            "checkInterval": self.checkInterval,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return test_step_table_dict

    def __str__(self):
        test_step_table_dict = {
            "stepId": self.id,
            "jobId": self.jobId,
            "stepName": self.stepName,
            "executeScriptPath": self.executeScriptPath,
            "executeScriptCmd": self.executeScriptCmd,
            "isSkipped": self.isSkipped,
            "checkInterval": self.checkInterval,
            "runFailedIsNeedContinue": self.runFailedIsNeedContinue,
            "updateTime": str(self.updateTime),
            "createTime": str(self.createTime)
        }
        return json.dumps(test_step_table_dict)


class TestPlanStatusTable(Base):
    __tablename__ = "test_plan_status_table"
    planId = Column(String(100), nullable=False)
    planName = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    executeStatus = Column(String(100), nullable=False)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testJobStatusList = relationship("TestJobStatusTable", back_populates="testPlanStatus")

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


class TestJobStatusTable(Base):
    __tablename__ = "test_job_status_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    jobId = Column(String(100), nullable=False)
    jobName = Column(String(100), nullable=False)
    planStatusId = Column(String(100), ForeignKey("test_plan_status_table.id"))
    executeStatus = Column(String(100), nullable=False)
    executeMachineIp = Column(String(100), nullable=False)
    processPid = Column(Integer, nullable=False)
    logFilePath = Column(String(100), nullable=False)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testPlanStatus = relationship("TestPlanStatusTable", back_populates="testJobStatusList")
    testStepStatusList = relationship("TestStepStatusTable", back_populates="testJobStatus")

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


class TestStepStatusTable(Base):
    __tablename__ = "test_step_status_table"
    jobStatusId = Column(String(100), ForeignKey("test_job_status_table.id"))
    stepId = Column(String(100), nullable=False)
    stepName = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    executeStatus = Column(String(100), nullable=False)
    processPid = Column(Integer, nullable=False)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testJobStatus = relationship("TestJobStatusTable", back_populates="testStepStatusList")

    def __str__(self):
        test_step_status_table_dir = {
            "stepStatusId": self.id,
            "jobStatusId": self.jobStatusId,
            "stepId": self.stepId,
            "processPid": self.processPid,
            "stepName": self.stepName,
            "executeStatus": self.executeStatus,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return json.dumps(test_step_status_table_dir)

    def __repr__(self):
        test_step_status_table_dir = {
            "stepStatusId": self.id,
            "jobStatusId": self.jobStatusId,
            "stepId": self.stepId,
            "processPid": self.processPid,
            "stepName": self.stepName,
            "executeStatus": self.executeStatus,
            "updateTime": self.updateTime,
            "createTime": str(self.createTime)
        }
        return test_step_status_table_dir


class TestMachineTable(Base):
    # TODO 增加一个机器资源自动采集功能
    __tablename__ = "test_machine_table"
    machineId = Column(Integer, primary_key=True, autoincrement=True)
    jobId = Column(String(100), ForeignKey("test_job_table.id"))
    ip = Column(String(100), nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    hostName = Column(String(100), nullable=True)
    cpuSize = Column(String(100), nullable=True)
    memorySize = Column(String(100), nullable=True)
    diskSize = Column(String(100), nullable=True)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)
    testJob = relationship("TestJobTable", back_populates="executeMachineIpList")

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


class User(Base):
    __tablename__ = "user_info_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    userName = Column(String(100), nullable=True)
    password = Column(String(100), nullable=True)
    role = Column(String(100), nullable=True)
    phone = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)
    updateTime = Column(TIMESTAMP, nullable=False)
    createTime = Column(TIMESTAMP, nullable=False)


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
    db_name = "testkeeper.db"
    sql = SQLalchemyDbOperation(db_path, db_name)
    sql.create_table()
    Base.metadata.create_all(sql.sqlalchemy_engine)
