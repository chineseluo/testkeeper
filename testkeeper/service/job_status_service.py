#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 17:36
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : job_status_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
import datetime
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.module.execute_status_module import ExecuteStatus
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestMachineTable
from testkeeper.exception.exception import *


class JobStatusService(SqlInterface):
    def __init__(self):
        super().__init__()
        self.shell_client = ShellClient()
        self.execute_result = {}
        self.__job_status_id = None
        self.__plan_status_id = None

    @property
    def job_status_id(self):
        return self.__job_status_id

    @job_status_id.setter
    def job_status_id(self, job_status_id):
        if job_status_id is None:
            raise TestKeeperArgvCheckException(f"参数job_status_id:{job_status_id}，不能为None！")
        if not isinstance(job_status_id, int):
            raise TestKeeperArgvCheckException(f"参数job_status_id:{job_status_id}，类型错误，应当为int类型！")
        self.__job_status_id = job_status_id

    @property
    def plan_status_id(self):
        return self.__plan_status_id

    @plan_status_id.setter
    def plan_status_id(self, plan_status_id):
        if plan_status_id is None:
            self.__plan_status_id = None
        else:
            try:
                self.__plan_status_id = int(plan_status_id)
            except Exception as e:
                logger.error(e)
                raise TestKeeperArgvCheckException(f"参数plan_status_id:{plan_status_id}，类型错误，应当为int类型！")

    def get_job_status_table_obj(self) -> TestJobStatusTable:
        job_status_table_obj = self.mul_session.query(TestJobStatusTable).filter_by(id=self.__job_status_id).first()
        return job_status_table_obj

    def get_test_job_status_list(self):
        if self.__plan_status_id is not None:
            test_job_status_list = [test_job.__repr__() for test_job in
                                    self.mul_session.query(TestJobStatusTable).filter(
                                        TestJobStatusTable.id == self.__plan_status_id).all()]
        else:
            test_job_status_list = [test_job.__repr__() for test_job in
                                    self.mul_session.query(TestJobStatusTable).filter().all()]
        return test_job_status_list

    def update_test_job_status(self, name: str, value: str):
        self.common_update_method(TestJobStatusTable, self.__job_status_id, name, value)

    def delete_test_job_status(self):
        self.mul_session.query(TestJobStatusTable).filter_by(id=self.__job_status_id).delete()
        self.mul_session.commit()
        logger.info(f"删除测试任务成功:{self.__job_status_id}")

    def generate_test_job_status_table_obj(self, test_job: TestJobTable, execute_status: ExecuteStatus):
        now_time = datetime.datetime.now()
        test_job_status_table_obj = TestJobStatusTable(
            jobId=test_job.id,
            jobName=test_job.jobName,
            executeStatus=execute_status,
            executeMachineIp="127.0.0.1",
            logFilePath="/tmp",
            updateTime=now_time,
            createTime=now_time
        )
        return test_job_status_table_obj
