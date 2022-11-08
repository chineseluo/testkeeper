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

    def insertTestJobTableData(self):
        planId = get_string_md5_add_time_stamp("plan")
        jobId = get_string_md5_add_time_stamp("job")
        test_job_table_obj = TestJobTable(
            planId=planId,
            jobId=jobId,
            jobName="job01",
            executeStatus="running",
            executeScriptPath="/tmp",
            executeScriptCmd="echo test",
            createTime=datetime.datetime.now()
        )
        test_plan_table_obj = TestPlanTable(
            planId=planId,
            projectName="测试项目",
            testPlanName="测试计划",
            cron="2 3 4 5 6",
            createTime=datetime.datetime.now()
        )
        test_job_table_list = []
        test_plan_table_list = []
        test_job_table_list.append(test_job_table_obj)
        test_plan_table_list.append(test_plan_table_obj)
        self.db_session.bulk_save_objects(test_job_table_list)
        self.db_session.bulk_save_objects(test_plan_table_list)
        self.db_session.commit()


if __name__ == '__main__':
    db_path = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))), "db")
    db_name = "testkeeper.db"
    md = MockData(db_path, db_name)
    md.insertTestJobTableData()
