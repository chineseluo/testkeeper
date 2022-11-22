#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
---------------------------------
@Project  : testkeeper
@File     : test_plan_conf.py
@Author   : 流星
---------------------------------
"""
from testkeeper.exception.exception import TestKeeperFileTypeException
from testkeeper.util.file_operation import FileOption
from pydantic import BaseModel
from typing import List, Optional


class TestMachine(BaseModel):
    """
    测试机器
    """
    ip: str
    username: str
    password: str
    hostName: str = None
    cpuSize: str = None
    memorySize: str = None
    diskSize: str = None


class TestStep(BaseModel):
    """
    测试步骤
    """
    stepName: str
    executeScriptPath: str
    executeScriptCmd: str
    runFailedIsNeedContinue: bool
    isSkipped: bool
    checkInterval: int = 10


class TestJob(BaseModel):
    """
    测试任务
    """
    jobName: str
    createUser: str
    executeScriptPath: str
    executeScriptCmd: str
    executeTimeout: int
    runFailedIsNeedContinue: bool
    isSkipped: bool
    checkInterval: int
    executeMachineIpList: List[TestMachine]
    TestStep: List[TestStep]


class TestPlan(BaseModel):
    """
    测试计划
    """
    version: Optional[str]
    projectName: str
    PlanName: str
    createUser: str
    isScheduledExecution: bool
    cron: str
    isConfigMessagePush: bool
    messagePushMethod: str
    messagePushWebhook: str
    TestJob: List[TestJob]

    def __init__(self, path: str):
        file_suffix = path.split(".")[-1]
        if file_suffix == "yml":
            test_plan_info = FileOption.read_yaml(path)
        elif file_suffix == "json":
            test_plan_info = FileOption.read_json(path)
        else:
            raise TestKeeperFileTypeException(f'TestKeeper提示：【{file_suffix}】不支持的文件类型!!!')
        super().__init__(**test_plan_info)
