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


class JobService(SqlInterface):

    def __init__(self):
        super().__init__()

    def delete_test_job(self, job_id: str):
        if job_id is None:
            logger.warning("job_id不能为空！")
        else:
            logger.info(job_id)
            self.mul_session.query(TestJobTable).filter_by(id=job_id).delete()
            self.mul_session.query(TestStepTable).filter_by(jobId=job_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试任务成功:{job_id}")

    def update_test_job(self, job_id: str, name: str, value: str):
        self.common_update_method(TestJobTable, job_id, name, value)

    def get_test_job_by_id(self, job_id: str):
        test_job_table_obj = self.mul_session.query(TestJobTable).filter(TestJobTable.id == job_id).first()
        return test_job_table_obj

    def get_test_job_list(self, plan_id: str = None):
        if plan_id is not None:
            test_job_list = [test_job.__repr__() for test_job in
                             self.mul_session.query(TestJobTable).filter(TestJobTable.planId == plan_id).all()]
        else:
            test_job_list = [test_job.__repr__() for test_job in
                             self.mul_session.query(TestJobTable).filter().all()]
        return test_job_list