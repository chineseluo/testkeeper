#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : testkeeper
@Time    : 11:46
@Auth    : 成都-阿木木
@Email   : 848257135@qq.com
@File    : job_service.py
@IDE     : PyCharm
------------------------------------
"""
from loguru import logger
from testkeeper.interface.sql_interface import SqlInterface
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable
from testkeeper.exception.exception import *


class JobService(SqlInterface):

    def __init__(self):
        super().__init__()
        self.__job_id = None
        self.__plan_id = None

    @property
    def job_id(self):
        return self.__job_id

    @job_id.setter
    def job_id(self, job_id):
        if job_id is None:
            raise TestKeeperArgvCheckException(f"参数job_id:{job_id}，不能为None！")
        if not isinstance(job_id, int):
            raise TestKeeperArgvCheckException(f"参数job_id:{job_id}，类型错误，应当为int类型！")
        self.__job_id = job_id

    @property
    def plan_id(self):
        return self.__plan_id

    @plan_id.setter
    def plan_id(self, plan_id):
        if plan_id is None:
            self.__plan_id = None
        else:
            if not isinstance(plan_id, int):
                raise TestKeeperArgvCheckException(f"参数plan_id:{plan_id}，类型错误，应当为int类型！")
            self.__plan_id = plan_id

    def delete_test_job(self):
        self.mul_session.query(TestJobTable).filter_by(id=self.__job_id).delete()
        self.mul_session.query(TestStepTable).filter_by(jobId=self.__job_id).delete()
        self.mul_session.commit()
        logger.info(f"删除测试任务成功:{self.__job_id}")

    def update_test_job(self, name: str, value: str):
        self.common_update_method(TestJobTable, self.__job_id, name, value)

    def get_test_job_by_id(self):
        test_job_table_obj = self.mul_session.query(TestJobTable).filter(TestJobTable.id == self.__job_id).first()
        return test_job_table_obj

    def get_test_job_list(self):
        if self.__plan_id is not None:
            test_job_list = [test_job.__repr__() for test_job in
                             self.mul_session.query(TestJobTable).filter(TestJobTable.planId == self.__plan_id).all()]
        else:
            test_job_list = [test_job.__repr__() for test_job in
                             self.mul_session.query(TestJobTable).filter().all()]
        return test_job_list
