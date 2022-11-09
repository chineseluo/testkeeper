#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:22
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : mock.py
@IDE     : PyCharm
------------------------------------
"""
import hashlib
import time
import os
import datetime
from typing import Text
from testkeeper.util.sqlalchemy_db_operation import SQLalchemyDbOperation
from testkeeper.module.sqlite_module import TestJobTable, TestPlanTable


def get_string_md5(string: str) -> str:
    string_time_stamp = string
    h = hashlib.md5(string_time_stamp.encode("utf-8"))
    md5 = h.hexdigest()
    return md5


def get_string_md5_add_time_stamp(string: str) -> str:
    time_stamp = int(round(time.time() * 1000))
    string_time_stamp = string + Text(time_stamp)
    h = hashlib.md5(string_time_stamp.encode("utf-8"))
    md5 = h.hexdigest()
    return md5


class MockData:

    def __init__(self, db_path, db_name):
        self.db_path = db_path
        self.db_name = db_name
        self.db_session = SQLalchemyDbOperation(self.db_path, self.db_name).use_connect()

    def insertTestJobTableData(self, plan_count: int, job_count: int):
        for plan_index in range(1, plan_count):
            test_plan_table_obj = TestPlanTable(
                projectName=f"测试项目{plan_index}",
                testPlanName=f"测试计划{plan_index}",
                createUser="成都-阿木木",
                isScheduledExecution=True,
                cron="2 3 4 5 6",
                isConfigMessagePush=True,
                messagePushMethod="企业微信",
                messagePushWebhook="www.baidu.com",
                createTime=datetime.datetime.now()
            )
            for i in range(1, job_count):
                test_job_table_obj = TestJobTable(
                    jobName=f"job0{i}",
                    createUser="成都-阿木木",
                    executeMachineIpList=f"127.0.0.{i}",
                    executeStatus="running",
                    executeScriptPath="/tmp",
                    executeScriptCmd="echo test",
                    executeTimeout=660,
                    runFailedIsNeedContinue=True,
                    isSkipped=False,
                    checkInterval=10,
                    createTime=datetime.datetime.now()
                )
                test_plan_table_obj.testJobs.append(test_job_table_obj)
            self.db_session.add(test_plan_table_obj)
            self.db_session.commit()


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
    db_name = "testkeeper.db"
    md = MockData(db_path, db_name)
    md.insertTestJobTableData(5, 10)
