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
from testkeeper.interface import sql_interface
from testkeeper.util.shell_utils import ShellClient
from testkeeper.module.sqlite_module import \
    TestJobTable, \
    TestPlanTable, \
    TestPlanStatusTable, \
    TestJobStatusTable, \
    TestStepStatusTable, \
    TestStepTable, TestMachineTable


class JobStatusService(sql_interface):
    def __init__(self):
        self.shell_client = ShellClient()
        self.execute_result = {}

    def get_job_status_table_obj(self, job_status_id: int) -> TestJobStatusTable:
        job_status_table_obj = self.mul_session.query(TestJobStatusTable).filter_by(id=job_status_id).first()
        return job_status_table_obj

    def get_test_job_status_list(self, plan_status_id: str = None):
        if plan_status_id is not None:
            test_job_status_list = [test_job.__repr__() for test_job in
                                    self.mul_session.query(TestJobStatusTable).filter(
                                        TestJobStatusTable.id == plan_status_id).all()]
        else:
            test_job_status_list = [test_job.__repr__() for test_job in
                                    self.mul_session.query(TestJobStatusTable).filter().all()]
        logger.info(test_job_status_list)
        return test_job_status_list

    def update_test_job_status(self, job_status_id: str, name: str, value: str):
        self.common_update_method(TestJobStatusTable, job_status_id, name, value)

    def delete_test_job_status(self, job_status_id: str):
        if job_status_id is None:
            logger.warning("job_id不能为空！")
        else:
            logger.info(job_status_id)
            self.mul_session.query(TestJobStatusTable).filter_by(id=job_status_id).delete()
            self.mul_session.query(TestStepStatusTable).filter_by(jobStatusId=job_status_id).delete()
            self.mul_session.commit()
            logger.info(f"删除测试任务成功:{job_status_id}")
